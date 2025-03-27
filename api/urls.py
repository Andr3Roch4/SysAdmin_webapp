from django.urls import path

from . import views

urlpatterns = [
    path("listar", views.listar, name="listar"),
    path("load", views.load, name="load"),
]