from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name="ایمیل",
        null=True,
        blank=True,
    )
    mobile = models.CharField(
        max_length=11,
        validators=[RegexValidator(r"^[0-9]{11}$")],
        verbose_name="شماره همراه",
        help_text="یازده رقمی بدون خط تیره. نمونه: 09121328462",
        null=True,
        blank=True,
    )
    is_email_verified = models.BooleanField(default=False)
    is_mobile_verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=4, null=True, blank=True)
    mobile_otp = models.CharField(max_length=4, null=True, blank=True)
    first_name = models.CharField(
        max_length=128, null=True, blank=True, verbose_name="نام"
    )
    last_name = models.CharField(
        max_length=128, null=True, blank=True, verbose_name="نام خانوادگی"
    )
    national_code = models.CharField(
        max_length=10, null=True, blank=True, verbose_name="کد ملی"
    )
    is_national_code_verified = models.BooleanField(
        default=False, verbose_name="تایید کد ملی"
    )
    birth_date = models.DateField(null=True, blank=True, verbose_name="تاریخ تولد")


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(
        max_length=128, null=True, blank=True, verbose_name="نام"
    )
    last_name = models.CharField(
        max_length=128, null=True, blank=True, verbose_name="نام خانوادگی"
    )
    mobile = models.CharField(max_length=11, verbose_name="شماره همراه")
    national_code = models.CharField(
        max_length=10, null=True, blank=True, verbose_name="کد ملی"
    )
    address = models.CharField(max_length=256, verbose_name="آدرس")
    city = models.CharField(max_length=64, verbose_name="شهر")
    province = models.CharField(max_length=64, verbose_name="استان")
    postal_code = models.CharField(max_length=10, verbose_name="کد پستی")
    number = models.CharField(max_length=10, verbose_name="شماره پلاک")
    unit = models.CharField(max_length=10, verbose_name="واحد")

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس ها"

    def __str__(self):
        return self.user.username

    def get_full_address(self):
        return f"{self.address} - {self.city} - {self.province} - {self.postal_code}"
