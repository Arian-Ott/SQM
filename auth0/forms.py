from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SuperUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    phone_number = forms.CharField(max_length=20, required=True)

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
