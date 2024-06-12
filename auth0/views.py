
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

import uuid

from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from Settings.models import Token
from .forms import RegisterForm, SuperUserCreationForm
from .models import UserRecovery


# Create your views here.
def sign_up(request):
    global tkna
    check = 1 if len(list(get_user_model().objects.all())) == 0 else 0
    rand_token = uuid.uuid4().hex

    if check == 1:
        tkna = UserRecovery()
        tkna.recovery_token = rand_token.encode("utf8")
        print(tkna.recovery_token_lul())

    if request.method == "POST":
        if check == 0:
            form = RegisterForm(request.POST)
        else:
            form = SuperUserCreationForm(request.POST)

            # request.user.user_permissions.add(Permission.objects.get(codename="su"))

        if form.is_valid():
            user = form.save()
            if check == 1:
                usr = User.objects.get(username=user.username)
                usr.is_superuser = True
                usr.save()
                tkna.user = usr

                tkna.save()

            tkn = Token.objects.create(owner=User.objects.get(pk=user.pk))
            tkn.save()
            login(request, user)

            return redirect("/")
    elif check == 0:
        form = RegisterForm()
    else:
        form = SuperUserCreationForm()

    return render(request, "registration/sign_up.html", {"form": form, "check": check, "rand_token": rand_token})


def logout_usr(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("/")
    else:

        return redirect("/login")
