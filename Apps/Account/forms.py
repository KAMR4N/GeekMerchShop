from django import forms
from .models import CustomUser, Address


class ProfileEditForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(), required=False, initial=None
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(), required=False, initial=None
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(), required=False, initial=None
    )

    day_of_birth = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(1, 32)],
        required=False,
    )
    month_of_birth = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(1, 13)],
        required=False,
    )
    year_of_birth = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(1980, 2021)],
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "mobile",
            "birth_date",
            "national_code",
        ]


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = [
            "first_name",
            "last_name",
            "mobile",
            "address",
            "city",
            "province",
            "postal_code",
            "number",
            "unit",
            "national_code",
        ]
