from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Produto, Distribuidor, Fornecedor, Transportador
from django.core import serializers
import csv

# Create your views here.

def listar(request):
    parametro = request.GET.get('nome', '').strip()                     # Qualquer nome a pesquisar
    category = request.GET.get('tipo', '').strip().lower()              # Tipo da categoria  (produto, fornecedor, etc.)
    local = request.GET.get('loc', '').strip()                          # local nos distribuidor, fornecedor e transportador
    categoria = request.GET.get('cat', '').strip()                      # Categoria do produto, em produto e fornecedor


    print("Parametros recebidos:")
    print(f"parametro: {parametro}")
    print(f"category: {category}")
    print(f"local: {local}")
    print(f"categoria: {categoria}")
    # Dicionário com os modelos disponíveis
    modelos = {
        "produto": Produto,
        "distribuidor": Distribuidor,
        "fornecedor": Fornecedor,
        "transportador": Transportador
    }

    # Modelos que possuem o campo `local`
    modelos_com_local = {"distribuidor", "fornecedor", "transportador"}

    data = {}

    # Se uma tipo for passado, filtra apenas nele **mas continua a buscar as outras**
    for key, model in modelos.items():
        print(f"Processando modelo: {key}")
        if category and key != category:  # Se `category` for passada, ignora os outros modelos
            continue
        if categoria and key not in ['produto', 'fornecedor']:
            print(f"Ignorando modelo {key} porque categoria foi informada.")
            continue  
        queryset = model.objects.all()
        
        if local and key not in modelos_com_local:
            continue
        
        # Filtra pelo nome, se fornecido
        if parametro:
            queryset = queryset.filter(nome__icontains=parametro)

        # Filtra pelo local, mas apenas se o modelo tiver esse campo
        if local and key in modelos_com_local:
            if hasattr(model, 'local'):  # Verifica se o modelo tem o campo `local`
                queryset = queryset.filter(local__icontains=local)
                print(f"Filtro de local aplicado: {local} para {key}")
        # Filtra pela categoria, mas apenas para Produto e Fornecedor
        if key == "fornecedor" and categoria:
            queryset = queryset.filter(cat__icontains=categoria)
        elif key == "produto" and categoria:
            queryset = queryset.filter(cat__icontains=categoria)

        if categoria and hasattr(model, 'cat'):
            queryset = queryset.filter(cat__icontains=categoria)
            print(f"Filtro de categoria aplicado: {categoria}")
   
        # Adiciona o resultado no dicionário
        data[key] = list(queryset.values())  

    # Verifica se a categoria ou localização não retornaram resultados e adiciona uma chave indicando isso
    for key, model in modelos.items():
        if not data.get(key):
            data[key + "_no_results"] = f"Sem {key} encontrado para o filtro usado"

    return JsonResponse(data, safe=False)


    #param = request.GET.get('q', '').strip()  # Obtém o parâmetro 'q' da URL
    #queryset = Produto.objects.all()
    #if param:  # Se 'q' foi passado na URL, aplica o filtro
        #queryset = queryset.filter(nome__icontains=param)
    #data = list(queryset.values())  
    #return JsonResponse(data, safe=False)
    #p=Produto.objects.all()                                         # Variavel data com todos os Produtos
    #d=Distribuidor.objects.all()                                    # Variavel data com todos os Distribuidores
    #f=Fornecedor.objects.all()                                      # Variavel data com todos os Fornecedores
    #t=Transportador.objects.all()

    #models = {
        #"produto": Produto,
        #"distribuidor": Distribuidor,
        #"fornecedor": Fornecedor,
        #"transportador": Transportador,
    #}
    #data = {
        #"produtos": list(p),
        #"distribuidores": list(d),
        #"fornecedores": list(f),
        #"transportadores": list(t),
    #}
                                                                    # Variavel data com todos os Transportadores
    #data = list(p) + list(d) + list(f) + list(t)                                      
    #json_data=serializers.serialize("json", data)                   # Transforma a data em json
    #return HttpResponse(json_data,# content_type='application/json') # Como já temos a data em json, temos de fazer Httpresponse e não JsonResponse


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