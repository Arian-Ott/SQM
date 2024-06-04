from base64 import urlsafe_b64decode, urlsafe_b64encode

import pymysql
from cryptography.fernet import Fernet
from django.contrib.auth import get_user_model
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from SQM import settings
from .forms import DBCreateForm, DBUserForm



def encrypt(data):
    settings.FERNET_KEY = Fernet.generate_key()
    return urlsafe_b64encode(Fernet(settings.FERNET_KEY).encrypt(str(data).encode("utf-8"))).decode('utf-8')

def decrypt(data):

    return Fernet(settings.FERNET_KEY).decrypt(urlsafe_b64decode(data).decode("utf-8")).decode("utf-8")

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
            form.save()

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

            return redirect(
                f"/dashboard/user-creation/{encrypt(tmp)}")
    return render(request, "dashboard/create_db.html", context={"form": DBCreateForm()})


@login_required(login_url='/login', redirect_field_name='n')
def create_db_user(request, temp):


    data = eval(decrypt(temp))

    print(data)
    conn = pymysql.connect(host=data["db_host"], port=data["db_port"], user=data["db_root"], password=data["root_pw"],
                           db=data["name"])
    cur = conn.cursor()
    if request.method == "POST":
        form = DBUserForm(request.POST)
        if form.is_valid():
            form.full_clean()
            frm = form.save(commit=False)
            frm.created_by = request.user
            form.save()

            data["username"] = form.cleaned_data.get("username")
            data["password"] = form.cleaned_data.get("password")

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
            return redirect(f"/dashboard/overview/{encrypt(data)}")
    return render(request, "dashboard/create_user.html", context={"form": DBUserForm()})

@login_required(login_url='/login', redirect_field_name='n')
def overview(request, temp):
    data = eval(decrypt(temp))

    return render(request, "dashboard/overview.html", context={"username": data["username"], "password": data["password"], "db_host": data["db_host"], "db_name": data["name"], "db_port": data["db_port"]} )
