from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path("login/", views.login_user, name="login"),
    path(
        "login-password/<int:user_id>/",
        views.login_user_password,
        name="login-password",
    ),
    path("login-otp/<int:user_id>/", views.login_user_otp, name="login-otp"),
    path("verify-otp/<int:user_id>/", views.check_otp, name="verify-otp"),
    path("forgot-otp/<int:user_id>/", views.forgot_otp, name="forgot-otp"),
    path("reset-password/<int:user_id>/", views.reset_password, name="reset-password"),
    path("logout/", views.logout_user, name="logout"),
    # Profile
    path("profile/dashboard/", views.profile, name="profile"),
    path("profile/orders/", views.profile_orders, name="profile-orders"),
    path("profile/address/", views.profile_address, name="profile-address"),
    path("profile/edit/", views.profile_edit, name="profile-edit"),
]
