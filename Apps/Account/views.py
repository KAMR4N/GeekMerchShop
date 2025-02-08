from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from Apps.Settings.models import GeneralSettings
from .models import CustomUser
from .utils import generate_otp, verify_otp
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
import re
from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm
from django.contrib import messages


def login_user(request):
    general_settings = GeneralSettings.objects.first()
    context = {
        "general_settings": general_settings,
    }
    if request.method == "POST":
        username = request.POST["username"]

        is_email = re.match(r"[^@]+@[^@]+\.[^@]+", username)
        is_mobile = re.match(r"^[0-9]{11}$", username)

        user = CustomUser.objects.filter(
            Q(email=username) if is_email else Q(mobile=username) if is_mobile else Q()
        ).first()

        if not user:
            user = CustomUser.objects.filter(username=username).first()
            if not user:
                user = CustomUser.objects.create_user(
                    username=username, mobile="", email=""
                )

        if user and user.is_mobile_verified:
            return redirect("login-password", user_id=user.id)
        else:
            mobile_otp = ""
            # Generate and save OTPs
            if is_email:
                user.email = username
                email_otp = generate_otp()
                user.email_otp = email_otp
            elif is_mobile:
                user.mobile = username
                mobile_otp = generate_otp()
                user.mobile_otp = mobile_otp

            user.save()

            # Send email OTP
            # send_mail(
            #     "Email Verification OTP",
            #     f"Your OTP for email verification is: {email_otp}",
            #     settings.EMAIL_HOST_USER,
            #     [email],
            #     fail_silently=False,
            # )

            # Send mobile OTP (you'll need to integrate with an SMS service)
            # For this example, we'll just print it

            print(f"Mobile OTP: {mobile_otp}")

        return redirect("verify-otp", user_id=user.id)

    return render(request, "Auth/login.html", context)


def login_user_password(request, user_id):
    general_settings = GeneralSettings.objects.first()
    context = {
        "general_settings": general_settings,
    }
    user = CustomUser.objects.get(id=user_id)

    if request.method == "POST":
        password = request.POST["password"]
        if password and user.check_password(password):
            login(request, user)
            return redirect("index")
        else:
            context["error"] = "Invalid password"

    context["user_id"] = user_id
    return render(request, "Auth/login-password.html", context)


def login_user_otp(request, user_id):
    general_settings = GeneralSettings.objects.first()
    context = {
        "general_settings": general_settings,
    }

    user = CustomUser.objects.get(id=user_id)
    if request.method == "POST":
        user_otp = request.POST["user_otp"]
        verified = False

        if user.mobile_otp and verify_otp(user_otp, user.mobile_otp):
            user.mobile_otp = None
            verified = True
        elif user.email_otp and verify_otp(user_otp, user.email_otp):
            user.email_otp = None
            verified = True

        if verified:
            user.save()
            login(request, user)
            return redirect("index")
        else:
            context["error"] = "Invalid OTP"
            return render(request, "Auth/login-otp.html", context)
    else:
        is_email = re.match(r"[^@]+@[^@]+\.[^@]+", user.username)
        is_mobile = re.match(r"^[0-9]{11}$", user.username)
        mobile_otp = ""
        # Generate and save OTPs
        if is_email:
            user.email = user.username
            email_otp = generate_otp()
            user.email_otp = email_otp
        elif is_mobile:
            user.mobile = user.username
            mobile_otp = generate_otp()
            user.mobile_otp = mobile_otp
        user.save()
        print(f"Mobile OTP: {mobile_otp}")
        context["user_id"] = user_id
        return render(request, "Auth/login-otp.html", context)


def check_otp(request, user_id):
    general_settings = GeneralSettings.objects.first()
    context = {
        "general_settings": general_settings,
    }
    user = CustomUser.objects.get(id=user_id)

    if request.method == "POST":
        user_otp = request.POST["user_otp"]
        verified = False

        if user.mobile_otp and verify_otp(user_otp, user.mobile_otp):
            user.is_mobile_verified = True
            user.mobile_otp = None
            verified = True
        elif user.email_otp and verify_otp(user_otp, user.email_otp):
            user.is_email_verified = True
            user.email_otp = None
            verified = True

        if verified:
            user.save()
            login(request, user)
            return redirect("index")
        else:
            context["error"] = "Invalid OTP"
            return render(request, "Auth/forgot-otp.html", context)
    context["user_id"] = user_id
    return render(request, "Auth/forgot-otp.html", context)


def forgot_otp(request, user_id):
    general_settings = GeneralSettings.objects.first()
    context = {
        "general_settings": general_settings,
    }

    user = CustomUser.objects.get(id=user_id)
    if request.method == "POST":
        user_otp = request.POST["user_otp"]
        verified = False

        if user.mobile_otp and verify_otp(user_otp, user.mobile_otp):
            user.mobile_otp = None
            verified = True
        elif user.email_otp and verify_otp(user_otp, user.email_otp):
            user.email_otp = None
            verified = True

        if verified:
            user.save()
            login(request, user)
            return redirect("reset-password", user_id=user.id)
        else:
            context["error"] = "Invalid OTP"
            return render(request, "Auth/forgot-otp.html", context)
    else:
        is_email = re.match(r"[^@]+@[^@]+\.[^@]+", user.username)
        is_mobile = re.match(r"^[0-9]{11}$", user.username)
        mobile_otp = ""
        # Generate and save OTPs
        if is_email:
            user.email = user.username
            email_otp = generate_otp()
            user.email_otp = email_otp
        elif is_mobile:
            user.mobile = user.username
            mobile_otp = generate_otp()
            user.mobile_otp = mobile_otp
        user.save()
        print(f"Mobile OTP: {mobile_otp}")
        context["user_id"] = user_id
        return render(request, "Auth/forgot-otp.html", context)


def reset_password(request, user_id):
    general_settings = GeneralSettings.objects.first()
    context = {
        "general_settings": general_settings,
    }

    user = CustomUser.objects.get(id=user_id)
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if not password or not confirm_password:
            context["error"] = "لطفا کلمه عبور و تکرار آن را وارد کنید"
            return render(request, "Auth/forgot-reset.html", context)
        if password != confirm_password:
            context["error"] = "کلمه عبور ها با هم مطابقت ندارند"
            return render(request, "Auth/forgot-reset.html", context)

        if password == confirm_password:
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect("index")
    context["user_id"] = user_id
    return render(request, "Auth/forgot-reset.html", context)


def logout_user(request):
    logout(request)
    return redirect("index")


def profile(request):
    context = {}
    return render(request, "Profile/_dashboard.html", context)


def profile_orders(request):
    context = {}
    return render(request, "Profile/_orders.html", context)


def profile_address(request):
    context = {}
    return render(request, "Profile/_address.html", context)


@login_required()
def profile_edit(request):
    context = {}
    username = request.user.username
    user = CustomUser.objects.filter(username=username)
    if not user.exists():
        raise Http404("کاربر مورد نظر یافت نشد")
    user = user.first()

    if request.method == "POST":
        edit_form = ProfileEditForm(
            request.POST or None,
            initial={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "mobile": user.mobile,
                "national_code": user.national_code,
                "birth_date": user.birth_date,
                "password": None,
                "new_password": None,
                "confirm_password": None,
            },
        )
        if edit_form.is_valid():
            first_name = edit_form.cleaned_data.get("first_name")
            last_name = edit_form.cleaned_data.get("last_name")
            email = edit_form.cleaned_data.get("email")
            mobile = edit_form.cleaned_data.get("mobile")
            national_code = edit_form.cleaned_data.get("national_code")
            birth_date = edit_form.cleaned_data.get("birth_date")
            current_password = edit_form.cleaned_data.get("password")
            new_password = edit_form.cleaned_data.get("new_password")
            confirm_password = edit_form.cleaned_data.get("confirm_password")
            
            
            day_of_birth = edit_form.cleaned_data.get("day_of_birth")
            month_of_birth = edit_form.cleaned_data.get("month_of_birth")
            year_of_birth = edit_form.cleaned_data.get("year_of_birth")
            
            print(edit_form.cleaned_data)

            if first_name != None:
                user.first_name = first_name
            if last_name != None:
                user.last_name = last_name
            if email != None:
                user.email = email
            if mobile != None:
                user.mobile = mobile
            if national_code != None:
                user.national_code = national_code
            if birth_date != None:
                user.birth_date = birth_date

            if current_password and new_password and confirm_password:
                if user.check_password(current_password):
                    if new_password == confirm_password:
                        user.set_password(new_password)
                        user.save()
                        context["status"] = "success"
                        messages.success(request, "تغییرات با موفقیت انجام شد")
                        return redirect("login")
                    else:
                        messages.error(request, "کلمه عبور با تکرار آن همخوانی ندارد")
                else:
                    messages.error(request, "کلمه عبور فعلی صحیح نمی باشد")
                    return redirect(request.META["HTTP_REFERER"])

            if not current_password:
                user.save()
                context["status"] = "success"
                messages.success(request, "تغییرات با موفقیت انجام شد")
                return redirect(request.META["HTTP_REFERER"])
        elif edit_form.errors:
            messages.error(request, edit_form.errors.as_text())
            return redirect(request.META["HTTP_REFERER"])

    return render(request, "Profile/_edit.html", context)
