from django import forms


class UserNewOrderForm(forms.Form):
    product_id = forms.IntegerField(
        widget=forms.HiddenInput(),
    )
    count = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "flex h-6 w-6 w-full select-none items-center justify-center bg-transparent text-center outline-none"
            }
        ),
        initial=1,
        disabled=False,
    )
