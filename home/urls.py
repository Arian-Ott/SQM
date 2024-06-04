from django.urls import path
from . import views

urlpatterns = [path("", views.prefunction, name="index")]
