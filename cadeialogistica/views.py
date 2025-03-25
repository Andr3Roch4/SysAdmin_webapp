from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, "home.html")
    #return HttpResponse("Vamos colocar aqui o menu (mostrar_menu) -> criar html idealmente")

def encomenda(request):
    return HttpResponse("Vamos colocar aqui a função de encomenda")

def comparar(request):
    return HttpResponse("Vamos colocar aqui a função de encomenda e da cadeia ideal")

def ideal(request):
    return HttpResponse("Vamos colocar aqui a função da cadeia ideal")

def criar(request):
    return HttpResponse("Vamos colocar aqui a função para criar objeto")