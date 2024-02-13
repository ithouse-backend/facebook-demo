from django import forms
from django.contrib.auth.forms import PasswordResetForm
from .models import User, Profile, About
from django.core.exceptions import (
    ValidationError,
)
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control my-2", "placeholder": "Enter Email"}
        ),
        label="",
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            return forms.ValidationError("There is no email")
        return email


class SetPasswordForm(forms.Form):
    """
    A form that lets a user set their password without entering the old
    password
    """

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    new_password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
                "placeholder": "New Password",
            }
        ),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control mt-2",
                "placeholder": "Repeat Password",
            }
        ),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

class CustomDateInput(forms.DateInput):
    input_type = 'date'

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'firstname',
            'lastname',
            'gender',
            'birthday'
        ]
        widgets = {
            "birthday": CustomDateInput()
        }

class UpdateProfilForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['banner', 'avatar', 'bio']

class UpdateAboutForm(forms.ModelForm):
    
    class Meta:
        model = About
        fields = ['company', 'position', 'city', 'description', 'school', 'is_graduated']