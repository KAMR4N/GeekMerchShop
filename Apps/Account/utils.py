import pyotp
from datetime import datetime, timedelta


def generate_otp():
    totp = pyotp.TOTP(
        pyotp.random_base32(), digits=4, interval=120
    )  # 2 minutes validity
    return totp.now()


def verify_otp(otp, user_otp):
    return otp == user_otp
