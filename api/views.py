from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Produto, Distribuidor, Fornecedor, Transportador
import csv

# Create your views here.

def listar(request):
    produtos=Produto.objects.all()
    data = [{'nome': produto.nome, 'peso_carregamento': produto.peso_carregamento, 'agua': produto.agua, 'luz': produto.luz, 'co2': produto.CO2, 'categoria': produto.cat} for produto in produtos]
    return JsonResponse(data, safe=False)


def load(request):
    prod="../csv/produto.csv"
    dist="../csv/distribuidor.csv"
    forn="../csv/fornecedor.csv"
    trans="../csv/transportador.csv"
    with open(prod, "r") as file:
        r=csv.DictReader(file)
        for row in r:
            Produto.objects.create(row)
    return HttpResponse("OK")