from django import forms
from .models import CustomUser


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
