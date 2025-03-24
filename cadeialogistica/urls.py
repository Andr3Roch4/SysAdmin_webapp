from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("/encomendar", views.encomenda, name="encomenda"),
    path("/comparar", views.comparar, name="comparar"),
    path("/ideal", views.ideal, name="ideal"),
    path("/criar", views.criar, name="criar"),
]