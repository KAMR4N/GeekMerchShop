from django.db import models
from treebeard.mp_tree import MP_Node, MP_NodeQuerySet
from django.db.models import Q

from Apps.Account.models import CustomUser

# Create your models here.


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
            | Q(tag__title__icontains=query)
        )
        return self.filter(lookup).distinct()


class Product(models.Model):
    is_variant = models.BooleanField(default=False)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(verbose_name="عنوان", max_length=128)
    title_en = models.CharField(
        verbose_name="عنوان انگلیسی", max_length=128, null=True, blank=True
    )
    slug = models.SlugField(
        verbose_name="عنوان url", blank=True, unique=True, allow_unicode=True
    )
    sku = models.CharField(verbose_name="کد کالا", max_length=128, unique=True)
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
    categories = models.ManyToManyField(
        Category, related_name="categories", verbose_name="دسته بندی ها"
    )
    parent = models.ForeignKey(
        "self",
        related_name="children",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="زیر دسته",
    )
    product_class = models.ForeignKey(
        "ProductClass",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="کلاس محصول",
    )
    attributes = models.ManyToManyField(
        "ProductAttribute",
        through="ProductAttributeValue",
        help_text="A product attribute defines a feature the product may have, like size...",
        verbose_name="ویژگی ها",
    )
    product_options = models.ManyToManyField(
        "Option",
        blank=True,
        help_text="Options are values that can be associated with a item "
        "something like a personalised message to be printed on "
        "a T-shirt.",
        verbose_name="گزینه ها",
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


class ProductClass(models.Model):
    """
    E.g. Books, DVDs and Toys. A product can only belong to one product class.
    """

    title = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=2048, null=True, blank=True)
    slug = models.SlugField(unique=True, allow_unicode=True)

    #: Digital products generally don't require their stock levels to be tracked and don't require shipping.
    track_stock = models.BooleanField(default=True)
    require_shipping = models.BooleanField(default=True)

    options = models.ManyToManyField("Option", blank=True)

    @property
    def has_attribute(self):
        return self.attributes.exists()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Product Class"
        verbose_name_plural = "Product Classes"


class ProductAttribute(models.Model):
    class AttributeTypeChoice(models.TextChoices):
        text = "text"
        integer = "integer"
        float = "float"
        option = "option"
        multi_option = "multi_option"

    product_class = models.ForeignKey(
        "ProductClass", on_delete=models.CASCADE, null=True, related_name="attributes"
    )
    title = models.CharField(max_length=64)
    type = models.CharField(
        max_length=16,
        choices=AttributeTypeChoice.choices,
        default=AttributeTypeChoice.text,
    )
    option_group = models.ForeignKey(
        "OptionGroup",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text='Select an option group if using type "Option" or "Multi Option"',
    )
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Product Attribute"
        verbose_name_plural = "Product Attributes"


class Option(models.Model):
    """
    An option that can be selected for an item when the product is added to the cart.

    For example,a personalised message to print on a T-shirt.
    """

    class OptionTypeChoice(models.TextChoices):
        text = "text"
        integer = "integer"
        float = "float"
        option = "option"
        multi_option = "multi_option"

    title = models.CharField(max_length=64)
    type = models.CharField(
        max_length=16, choices=OptionTypeChoice.choices, default=OptionTypeChoice.text
    )
    option_group = models.ForeignKey(
        "OptionGroup", on_delete=models.PROTECT, null=True, blank=True
    )
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Option"
        verbose_name_plural = "Option"


class OptionGroup(models.Model):
    """
    Defines a group of options that collectively may be used as an
    attribute type

    For example, Language
    """

    title = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Option Group"
        verbose_name_plural = "Option Groups"


class OptionGroupValue(models.Model):
    """
    Provides an option within an option group for an attribute type
    Examples: In a Language group, English, Greek, French
    """

    title = models.CharField(max_length=255, db_index=True)
    group = models.ForeignKey("OptionGroup", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Option Group Value"
        verbose_name_plural = "Option Group Values"


class ProductAttributeValue(models.Model):
    """
    m2m relationship between Product and ProductAttribute. This specifies the value of the attribute for
    a particular product
    """

    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    attribute = models.ForeignKey("ProductAttribute", on_delete=models.CASCADE)

    value_text = models.TextField(null=True, blank=True)
    value_integer = models.IntegerField(null=True, blank=True)
    value_float = models.FloatField(null=True, blank=True)
    value_option = models.ForeignKey(
        "OptionGroupValue", on_delete=models.PROTECT, null=True, blank=True
    )
    value_multi_option = models.ManyToManyField(
        "OptionGroupValue", blank=True, related_name="multi_valued_attribute_value"
    )

    class Meta:
        verbose_name = "Attribute Value"
        verbose_name_plural = "Attribute Values"
        unique_together = ("product", "attribute")


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
