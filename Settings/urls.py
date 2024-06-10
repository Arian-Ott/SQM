from django.urls import path
from .views import *
urlpatterns = [

    path('db/', prefunction, name='index'),
    path("user-creation/<str:temp>", create_db_user),
    path("overview/<str:temp>", overview, name='overview'),
    path("",dashboard),
    path("i/<str:temp>", details)
]