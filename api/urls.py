from django.urls import path

from . import views

urlpatterns = [
    #path("listar", views.listar, name="listar"),
    path("produto", views.produto, name="produto"),
    path("fornecedor", views.fornecedor, name="fornecedor"),
    path("distribuidor", views.distribuidor, name="distribuidor"),
    path("transportador", views.transportador, name="transportador"),
    path("impacto", views.impacto, name="impacto"),
    path("ideal", views.ideal, name="ideal")
    #path("load", views.load, name="load"),
]