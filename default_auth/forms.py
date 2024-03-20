"""
Forms for authorization and registration.
"""

from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm


class SignupForm(ModelForm):
    """
    Form for registering a new user.
    """

    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Your Email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Re-Password"})
    )

    class Meta:
        """
        Form model with fields.
        """

        model = User
        fields = ("username", "email", "password", "password2")


class LoginForm(forms.Form):
    """
    Authorization form.
    """

    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Name"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}))
