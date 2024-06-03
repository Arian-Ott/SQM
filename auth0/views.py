from django.contrib.auth import login, get_user_model
from django.contrib.auth.models import Permission

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
            request.user.user_permissions.add(Permission.objects.get(codename="su"))

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect("/")
    elif check == 0:
        form = RegisterForm()
    else:
        form = SuperUserCreationForm()

    return render(request, "registration/sign_up.html", {"form": form, "check": check})
