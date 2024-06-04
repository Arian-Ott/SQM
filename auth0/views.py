from django.contrib.auth import login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import RegisterForm, SuperUserCreationForm


# Create your views here.
def sign_up(request):
    check = 1 if len(list(get_user_model().objects.all())) == 0 else 0

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
            login(request, user)

            return redirect("/")
    elif check == 0:
        form = RegisterForm()
    else:
        form = SuperUserCreationForm()

    return render(request, "registration/sign_up.html", {"form": form, "check": check})



def logout_usr(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("/")
    else:

        return redirect("/login")
