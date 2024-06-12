
#   <one line to give the program's name and a brief idea of what it does.>
#      Copyright (c) 2024,.  Arian Ott
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from SQM.settings import DEBUG


class SuperUserCreationForm(UserCreationForm):
    if DEBUG:
        username = forms.CharField(required=True, initial="admin")
        email = forms.EmailField(required=True, initial="admin@sqm.com")
        first_name = forms.CharField(max_length=20, required=True, initial="Günter")
        last_name = forms.CharField(max_length=20, required=True, initial="Maier")
        phone_number = forms.CharField(max_length=20, required=True, initial="+49 123 45678")
        security_key = forms.CharField(max_length=255,
                                       help_text="Please input a security key which will be used to reset your account. This version does not support a mail system. Please keep your security key at a place where you will find it later. Without this key there is no way of recovering your account.",
                                       required=False, disabled=True)
    else:
        # email = forms.EmailField(required=True, initial="admin@sqm.com")
        first_name = forms.CharField(max_length=20, required=True)
        last_name = forms.CharField(max_length=20, required=True)

        phone_number = forms.CharField(max_length=20, required=True)

        security_key = forms.CharField(max_length=255,
                                       help_text="Please input a security key which will be used to reset your account. This version does not support a mail system. Please keep your security key at a place where you will find it later. Without this key there is no way of recovering your account.",
                                       required=False, disabled=True)
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
    email = forms.EmailField(required=True, initial="john.doe@sqm.com")
    first_name = forms.CharField(max_length=255, required=True, initial="John")
    last_name = forms.CharField(max_length=255, required=True, initial="Doe")
    username = forms.CharField(max_length=255, required=True, initial="john.doe")

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
