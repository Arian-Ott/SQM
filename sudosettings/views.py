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
from base64 import urlsafe_b64decode, urlsafe_b64encode

from cryptography.fernet import Fernet
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from Settings.models import TempToken


def encrypt(data, uid):
    fernet_key = TempToken.objects.get(uuid=uid).fernet
    return urlsafe_b64encode(Fernet(fernet_key).encrypt(str(data).encode("utf-8"))).decode('utf-8')


def decrypt(data, uid):
    fernet_key = TempToken.objects.get(uuid=uid).fernet

    return Fernet(fernet_key).decrypt(urlsafe_b64decode(data).decode("utf-8")).decode("utf-8")


def _check_user(request):
    return True if request.user.is_superuser else False


@login_required(login_url="/login")
def main(request):
    if _check_user(request):
        sudo_view = [{"title": "User Management", "url": "sudo/users/", "button": "User Console"},
                     {"title": "Server", "url": "sudo/servers/", "button": "Server Management"},
                     {"title": "Sudo Settings", "url": "sudo/sudo-settings/", "button": "Sudo Settings"},
                     {"title": "System Information", "url": "sudo/system/", "button": "System Information"},
                     {"title": "Plugins", "url": "sudo/plugins/", "button": "Manage Plugins"}]
        return render(request, 'overview/overview.html', context={"sudo_view": sudo_view})
    return redirect("/", status_code=418)


@login_required(login_url="/login")
def user_console(request):
    token = TempToken()
    token.save()
    uuid = token.uuid

    users = [{"request_id": request.user.id, "user_id": x.id, "username": x.username, "first_name": x.first_name,
              "last_name": x.last_name, "is_superuser": x.is_superuser,
              "last_logged_in_date": str(x.last_login.strftime("%d.%m.%Y")),
              "last_login_time": x.last_login.strftime("%H:%M:%S"), "is_active": x.is_active, "uuid": uuid,
              "url": encrypt(x.pk, uuid)} for x in
             User.objects.all().order_by('-date_joined')]

    print(users)

    return render(request, 'userconsole/console.html', context={"users": reversed(users)})


@login_required(login_url="/login")
def user_edit(request, session, uuid):
    try:
        user_id = decrypt(session, uuid)
    except:
        return HttpResponseForbidden(reason="Invalid auth header", status=403, content_type="error",
                                     content="Invalid UUID")
    user_id = eval(user_id)

    TempToken.objects.get(uuid=uuid).delete()
    print(user_id)
    return redirect("/")
