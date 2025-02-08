from django.db import models
from django.core.validators import FileExtensionValidator


# Create your models here.
class GeneralSettings(models.Model):
    header_logo_image = models.FileField(
        upload_to="Assets/images/",
        validators=[FileExtensionValidator(["svg"])],
        null=True,
        blank=True,
        verbose_name="(هدر) تصویر لوگو",
    )
    header_menu_items = models.JSONField(
        null=True,
        blank=True,
        verbose_name="(هدر) آیتم‌های منو",
        help_text="لیستی از آیتم‌های منو به صورت JSON",
    )
    footer_tel_text = models.CharField(
        max_length=256, null=True, blank=True, verbose_name="(فوتر) متن تلفن پشتیبانی"
    )
    footer_short_text = models.CharField(
        max_length=256, null=True, blank=True, verbose_name="(فوتر) متن کوتاه"
    )
    footer_mail_text = models.CharField(
        max_length=256, null=True, blank=True, verbose_name="(فوتر) متن خبرنامه"
    )
    footer_col1_menu_items = models.JSONField(
        null=True,
        blank=True,
        verbose_name="(فوتر) آیتم‌های منو ستون اول",
        help_text="لیستی از آیتم‌های منو به صورت JSON",
    )
    footer_col2_menu_items = models.JSONField(
        null=True,
        blank=True,
        verbose_name="(فوتر) آیتم‌های منو ستون دوم",
        help_text="لیستی از آیتم‌های منو به صورت JSON",
    )
    footer_copyright_text = models.CharField(
        max_length=256, null=True, blank=True, verbose_name="(فوتر) متن کپی رایت"
    )
    terms_and_conditions = models.TextField(
        null=True,
        blank=True,
        verbose_name="قوانین و شرایط استفاده",
    )
    about = models.TextField(
        null=True,
        blank=True,
        verbose_name="درباره ما",
    )
    class Meta:
        verbose_name = "تنظیمات عمومی"
        verbose_name_plural = "تنظیمات عمومی"


class Banner(models.Model):
    POSITION_CHOICES = (
        ("S", "Slider"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
    )
    image = models.ImageField(
        upload_to="Assets/images/", null=True, blank=True, verbose_name="تصویر"
    )
    image_alt = models.CharField(
        max_length=256, null=True, blank=True, verbose_name="عنوان تصویر"
    )
    link = models.URLField(max_length=256, null=True, blank=True, verbose_name="آدرس")
    position = models.CharField(
        max_length=1,
        null=True,
        blank=True,
        choices=POSITION_CHOICES,
        verbose_name="مکان",
    )

    class Meta:
        verbose_name = "بنر"
        verbose_name_plural = "بنر ها"


class CategoryImage(models.Model):
    image = models.ImageField(
        upload_to="Categories/", null=True, blank=True, verbose_name="تصویر"
    )
    image_alt = models.CharField(
        max_length=256, null=True, blank=True, verbose_name="عنوان تصویر"
    )
    category = models.ForeignKey(
        "Shop.Category", on_delete=models.CASCADE, verbose_name="دسته بندی"
    )

    class Meta:
        verbose_name = "تصویر دسته بندی"
        verbose_name_plural = "تصویر های دسته بندی"