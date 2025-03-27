from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Produto, Distribuidor, Fornecedor, Transportador
from django.core import serializers
from django.db.models import Q 
import csv

# Create your views here.

def listar(request):
    p=Produto.objects.all()                                         # Variavel data com todos os Produtos
    d=Distribuidor.objects.all()                                    # Variavel data com todos os Distribuidores
    f=Fornecedor.objects.all()                                      # Variavel data com todos os Fornecedores
    t=Transportador.objects.all()                                   # Variavel data com todos os Transportadores
    data = list(p) + list(d) + list(f) + list(t)                                      
    json_data=serializers.serialize("json", data)                   # Transforma a data em json
    return HttpResponse(json_data, content_type='application/json') # Como já temos a data em json, temos de fazer Httpresponse e não JsonResponse


def load(request):
    prod="csv/produto.csv"
    dist="csv/distribuidor.csv"
    forn="csv/fornecedor.csv"
    trans="csv/transportador.csv"
    #with open(trans, "r") as file:
        #r=csv.DictReader(file)
        #for row in r:
            #Transportador.objects.create(**row)
    return HttpResponse("OK")