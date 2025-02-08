from django.db import models
from treebeard.mp_tree import MP_Node, MP_NodeQuerySet
from django.db.models import Q

from Apps.Account.models import CustomUser


class CategoryQuerySet(MP_NodeQuerySet):
    """
    Excludes non-active categories
    """

    def public(self):
        return self.filter(is_active=True)


class Category(MP_Node):
    """
    A product category used for navigation
    """

    title = models.CharField(max_length=255, db_index=True, verbose_name="عنوان")
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name="عنوان url")
    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال",
    )
    objects = CategoryQuerySet.as_manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    @property
    def get_url(self):
        return f"/category/{self.slug}"


class ProductManager(models.Manager):

    def get_product_by_slug(self, slug):
        return self.filter(slug=slug).first()

    def get_product_by_id(self, id):
        return self.filter(pk=id).first()

    def get_related_products_by_product_category(self, product):
        return (
            self.filter(categories__title__icontains=product.categories.first().title)
            .exclude(pk=product.pk)
            .distinct()
        )

    def search(self, query):
        lookup = (
            Q(title__icontains=query)
            | Q(description__icontains=query)
        )
        return self.filter(lookup).distinct()


class Product(models.Model):
    title = models.CharField(verbose_name="عنوان", max_length=128)
    title_en = models.CharField(
        verbose_name="عنوان انگلیسی", max_length=128, null=True, blank=True
    )
    slug = models.SlugField(
        verbose_name="عنوان url", blank=True, unique=True, allow_unicode=True
    )
    quantity = models.PositiveIntegerField(verbose_name="موجودی", default=0)
    price = models.PositiveIntegerField(verbose_name="قیمت", default=0)
    is_special = models.BooleanField(default=False, verbose_name="ویژه")
    discount_percent = models.PositiveIntegerField(
        verbose_name="درصد تخفیف", default=0, null=True, blank=True
    )
    discounted_price = models.PositiveIntegerField(
        verbose_name="قیمت با تخفیف", default=0, null=True, blank=True
    )
    is_suggested = models.BooleanField(default=False, verbose_name="پیشنهادی")
    description = models.TextField(verbose_name="توضیحات", blank=True, null=True)

    color = models.CharField(
        verbose_name="رنگ", max_length=128, null=True, blank=True
    )
    size = models.CharField(
        verbose_name="اندازه", max_length=128, null=True, blank=True
    )
    material = models.CharField(
        verbose_name="جنس", max_length=128, null=True, blank=True
    )
    extra_features = models.TextField(verbose_name="ویژگی های بیشتر", null=True, blank=True)

    categories = models.ManyToManyField(
        Category, related_name="categories", verbose_name="دسته بندی ها"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=True,
        null=True,
        blank=True,
        verbose_name="تاریخ ایجاد",
    )

    objects = ProductManager()

    @property
    def main_image(self):
        if self.images.exists():
            return self.images.first()
        else:
            return None

    @property
    def get_url(self):
        return f"/shop/product/{self.slug}"

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        width_field="width",
        height_field="height",
        upload_to="Products/",
        blank=True,
        null=True,
    )
    alt_text = models.CharField(max_length=512, null=True, blank=True)
    width = models.IntegerField(editable=False, null=True, blank=True)
    height = models.IntegerField(editable=False, null=True, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order",)
        verbose_name = "تصویر محصول"
        verbose_name_plural = "تصویر های محصول"

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

        for index, image in enumerate(self.product.images.all()):
            image.display_order = index
            image.save()

    def __str__(self):
        return f"{self.product.title} - {self.alt_text}"


class Order(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="مالک")
    is_paid = models.BooleanField(verbose_name="پرداخت شده / نشده")
    payment_date = models.DateTimeField(
        blank=True, null=True, verbose_name="تاریخ پرداخت"
    )

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبد های کاربران"

    def __str__(self):
        return self.owner.get_username()

    def get_total_price(self):
        amount = 0
        for detail in self.orderdetail_set.all():
            amount += detail.price * detail.count
        return amount


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="سبد خرید")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    price = models.IntegerField(verbose_name="قیمت محصول")
    count = models.IntegerField(verbose_name="تعداد محصول")

    def get_detail_sum(self):
        return self.count * self.price

    class Meta:
        verbose_name = "جزئیات سفارش"
        verbose_name_plural = "جزئیات سفارشات"

    def __str__(self):
        return self.product.title
