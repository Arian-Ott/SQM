from django.forms import ModelForm

from .models import DB, DBUser


class DBCreateForm(ModelForm):
    class Meta:
        model = DB


        fields = ["name", "db_host", "db_port", "db_root", "root_pw"]

class DBUserForm(ModelForm):
    class Meta:
        model = DBUser
        fields = ["username", "password"]
