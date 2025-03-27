from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Produto, Distribuidor, Fornecedor, Transportador
from django.core import serializers
import csv

# Create your views here.

def listar(request):
    data=Produto.objects.all()                                      # Variavel data com todos os Produtos
    json_data=serializers.serialize("json", data)                   # Transforma a data em json
    return HttpResponse(json_data, content_type='application/json') # Como já temos a data em json, temos de fazer Httpresponse e não JsonResponse


def load(request):
    prod="../csv/produto.csv"
    dist="../csv/distribuidor.csv"
    forn="../csv/fornecedor.csv"
    trans="../csv/transportador.csv"
    with open(prod, "r") as file:
        r=csv.DictReader(file)
        for row in r:
            Produto.objects.create(**row)
    return HttpResponse("OK")