# Generated by Django 4.2.18 on 2025-02-08 16:36

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("Shop", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Banner",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="Assets/images/",
                        verbose_name="تصویر",
                    ),
                ),
                (
                    "image_alt",
                    models.CharField(
                        blank=True,
                        max_length=256,
                        null=True,
                        verbose_name="عنوان تصویر",
                    ),
                ),
                (
                    "link",
                    models.URLField(
                        blank=True, max_length=256, null=True, verbose_name="آدرس"
                    ),
                ),
                (
                    "position",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("S", "Slider"),
                            ("1", "1"),
                            ("2", "2"),
                            ("3", "3"),
                            ("4", "4"),
                        ],
                        max_length=1,
                        null=True,
                        verbose_name="مکان",
                    ),
                ),
            ],
            options={
                "verbose_name": "بنر",
                "verbose_name_plural": "بنر ها",
            },
        ),
        migrations.CreateModel(
            name="GeneralSettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "header_logo_image",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="Assets/images/",
                        validators=[
                            django.core.validators.FileExtensionValidator(["svg"])
                        ],
                        verbose_name="(هدر) تصویر لوگو",
                    ),
                ),
                (
                    "header_menu_items",
                    models.JSONField(
                        blank=True,
                        help_text="لیستی از آیتم\u200cهای منو به صورت JSON",
                        null=True,
                        verbose_name="(هدر) آیتم\u200cهای منو",
                    ),
                ),
                (
                    "footer_tel_text",
                    models.CharField(
                        blank=True,
                        max_length=256,
                        null=True,
                        verbose_name="(فوتر) متن تلفن پشتیبانی",
                    ),
                ),
                (
                    "footer_short_text",
                    models.CharField(
                        blank=True,
                        max_length=256,
                        null=True,
                        verbose_name="(فوتر) متن کوتاه",
                    ),
                ),
                (
                    "footer_mail_text",
                    models.CharField(
                        blank=True,
                        max_length=256,
                        null=True,
                        verbose_name="(فوتر) متن خبرنامه",
                    ),
                ),
                (
                    "footer_col1_menu_items",
                    models.JSONField(
                        blank=True,
                        help_text="لیستی از آیتم\u200cهای منو به صورت JSON",
                        null=True,
                        verbose_name="(فوتر) آیتم\u200cهای منو ستون اول",
                    ),
                ),
                (
                    "footer_col2_menu_items",
                    models.JSONField(
                        blank=True,
                        help_text="لیستی از آیتم\u200cهای منو به صورت JSON",
                        null=True,
                        verbose_name="(فوتر) آیتم\u200cهای منو ستون دوم",
                    ),
                ),
                (
                    "footer_copyright_text",
                    models.CharField(
                        blank=True,
                        max_length=256,
                        null=True,
                        verbose_name="(فوتر) متن کپی رایت",
                    ),
                ),
                (
                    "terms_and_conditions",
                    models.TextField(
                        blank=True, null=True, verbose_name="قوانین و شرایط استفاده"
                    ),
                ),
                (
                    "about",
                    models.TextField(blank=True, null=True, verbose_name="درباره ما"),
                ),
            ],
            options={
                "verbose_name": "تنظیمات عمومی",
                "verbose_name_plural": "تنظیمات عمومی",
            },
        ),
        migrations.CreateModel(
            name="CategoryImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="Categories/",
                        verbose_name="تصویر",
                    ),
                ),
                (
                    "image_alt",
                    models.CharField(
                        blank=True,
                        max_length=256,
                        null=True,
                        verbose_name="عنوان تصویر",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Shop.category",
                        verbose_name="دسته بندی",
                    ),
                ),
            ],
            options={
                "verbose_name": "تصویر دسته بندی",
                "verbose_name_plural": "تصویر های دسته بندی",
            },
        ),
    ]
