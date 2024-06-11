
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

import pymysql
from cryptography.fernet import Fernet
from django.contrib.auth import get_user_model
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import DBCreateForm, DBUserForm
from .models import DB, DBUser, TempToken, Token, UserTemp


def encrypt(data, uid):
    fernet_key = TempToken.objects.get(uuid=uid).fernet
    return urlsafe_b64encode(Fernet(fernet_key).encrypt(str(data).encode("utf-8"))).decode('utf-8')


def decrypt(data, uid):
    fernet_key = TempToken.objects.get(uuid=uid).fernet

    return Fernet(fernet_key).decrypt(urlsafe_b64decode(data).decode("utf-8")).decode("utf-8")


def prefunction(request):
    if len(get_user_model().objects.all()) == 0:
        return redirect("/hello")
    return create_db(request)


@login_required(login_url='/login', redirect_field_name='n')
def create_db(request):
    if request.method == "POST":
        form = DBCreateForm(request.POST)
        if form.is_valid():
            form.full_clean()
            frm = form.save(commit=False)
            frm.owner = request.user
            frm.save()

            try:

                conn = pymysql.connect(host=form.cleaned_data['db_host'], user=form.cleaned_data['db_root'],
                                       password=form.cleaned_data['root_pw'], port=form.cleaned_data['db_port'])
                cur = conn.cursor()
                query = f" CREATE DATABASE IF NOT EXISTS `{form.cleaned_data['name']}`; "  # + f"USE `{form.cleaned_data['name']};"
                cur.execute(query)
                conn.commit()
                conn.close()

            except pymysql.Error as e:
                return render(request, "dashboard/create_db.html", context={"form": DBCreateForm(), "error": str(e)})
            tmp = dict(form.cleaned_data)
            tmp["id"] = frm.pk
            token = TempToken()
            token.save()
            uid = token.uuid
            request.session['uid'] = str(uid)
            return redirect(
                f"/dashboard/user-creation/{encrypt(tmp, uid)}")
    return render(request, "dashboard/create_db.html", context={"form": DBCreateForm()})


@login_required(login_url='/login', redirect_field_name='n')
def create_db_user(request, temp):
    uid = request.session['uid']
    print(uid)
    data = eval(decrypt(temp, uid))

    conn = pymysql.connect(host=data["db_host"], port=data["db_port"], user=data["db_root"], password=data["root_pw"],
                           db=data["name"])
    cur = conn.cursor()
    if request.method == "POST":
        form = DBUserForm(request.POST)
        if form.is_valid():
            form.full_clean()
            frma = form.save(commit=False)
            frma.created_by = request.user
            frma.save()
            print(frma.pk)
            data["username"] = form.cleaned_data.get("username")
            data["password"] = form.cleaned_data.get("password")
            data["db_uid"] = frma.pk
            try:
                with conn.cursor() as cur:
                    # Create user query
                    create_user_query = "CREATE USER %s@'%%' IDENTIFIED BY %s;"
                    cur.execute(create_user_query, (data["username"], data["password"]))
                    conn.commit()

                    # Grant privileges query
                    grant_privileges_query = "GRANT ALL PRIVILEGES ON `%s`.* TO %s@'%%';"
                    cur.execute(grant_privileges_query, (data["name"], data["username"]))
                    conn.commit()
            finally:
                conn.close()
                TempToken.objects.get(uuid=uid).delete()

                token = TempToken()
                token.save()
                uid = token.uuid
                request.session['uid'] = str(uid)
            return redirect(f"/dashboard/overview/{encrypt(data, uid)}")
    return render(request, "dashboard/create_user.html", context={"form": DBUserForm()})


@login_required(login_url='/login', redirect_field_name='n')
def overview(request, temp):
    uid = request.session["uid"]
    data = eval(decrypt(temp, uid))
    print(data)
    usr = UserTemp()
    usr.added_by = request.user
    usr.db = DB.objects.get(pk=data["id"])
    usr.db_user = DBUser.objects.get(pk=data["db_uid"])
    usr.save()
    TempToken.objects.get(uuid=uid).delete()
    del request.session["uid"]
    return render(request, "dashboard/overview.html",
                  context={"username": data["username"], "password": data["password"], "db_host": data["db_host"],
                           "db_name": data["name"], "db_port": data["db_port"]})


@login_required(login_url='/login')
def dashboard(request):
    dbs = DB.objects.filter(owner_id=request.user.pk)
    tmp =[]
    for a in dbs:
        tmp.append({"name": a.name,"host":a.db_host,"port":a.db_port, "user": a.db_root, "overview":a.url_id, "del": a.revocation_id})
    print(tmp)
    return render(request, "dashboard/dashboard.html", context={"dbs": tmp})

@login_required(login_url="/login")
def details(request, temp):
    try:

        db = DB.objects.get(url_id=temp)
        pw = db.root_pw
        _user_fernet = Token.objects.get(owner_id=request.user.pk).fernet
        Fernet(Token.objects.get(owner_id=request.user.pk).fernet).decrypt(str(pw).encode())
        return render(request, "dashboard/details.html",
                      context={"name": db.name, "host": db.db_host, "root": db.db_root, "db_port": db.db_port,
                               "dbs": 1, "root_pw": pw})

    except DB.DoesNotExist:
        return render(request, "dashboard/details.html", context={"dbs": 0})






