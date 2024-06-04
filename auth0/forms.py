from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SuperUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    security_key = forms.CharField(max_length=255, required=True, help_text="Please input a security key which will be used to reset your account. This version does not support a mail system. Please keep your security key at a place where you will find it later. Without this key there is no way of recovering your account.")
    class Meta:
        model = User


        fields = [
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "password1",
            "password2",
            "security_key"
        ]



class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]
