from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
import os
import dotenv


# Create your views here.
def prefunction(request):
    if len(get_user_model().objects.all()) == 0:
        return redirect("/hello")
    return index(request)

@login_required(login_url="/login")
def index(request):
    dotenv.load_dotenv("./env.env")
    data = {}
    data["version"] = os.getenv("SQM_VERSION")

    data["auth"] = 1
    data["username"] = request.user.username


    return render(request, "home/home_1.html", context=data)
