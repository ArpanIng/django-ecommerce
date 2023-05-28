from django import forms

from .models import Account


class RegistrationModelForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter Password",
            },
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
            },
        )
    )

    class Meta:
        model = Account
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password",
            "confirm_password",
        ]

    def __init__(self, *args, **kwargs):
        """Applies form-control class to all input attributes"""
        super(RegistrationModelForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["placeholder"] = "First Name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Last Name"
        self.fields["email"].widget.attrs["placeholder"] = "email@address.com"
        self.fields["phone_number"].widget.attrs["placeholder"] = "Phone number"
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned_data = super(RegistrationModelForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            # Render errors as {{ form.non_field_errors }}
            raise forms.ValidationError(message="Password does not match.")
