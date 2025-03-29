from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Produto, Distribuidor, Fornecedor, Transportador
from django.core import serializers
import csv
from django.views.decorators.csrf import csrf_exempt
import json

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

@csrf_exempt
def produto(request):
    if request.method == "GET":

        nome=request.GET.get('nome', '').strip().lower()
        categoria=request.GET.get('cat', '').strip()
        id=request.GET.get('id', '').strip()

        p=Produto.objects.all().filter(nome__icontains=nome, cat__icontains=categoria, id__icontains=id)

        return JsonResponse({"produto":list(p.values())})
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)

            nome=data.get('nome', '').strip().capitalize()
            peso_carregamento=int(data.get('peso_carregamento', 0)) 
            agua=int(data.get('agua', 0)) 
            luz=int(data.get('luz', 0))
            co2=int(data.get('CO2', 0))
            cat=data.get('cat', '').strip().capitalize()

            if Produto.objects.filter(nome__iexact=nome).exists():
                return JsonResponse({"erro": "Este produto já existe!"}, status=400)
            
            produto=Produto.objects.create(
                nome=nome,
                peso_carregamento=peso_carregamento,
                agua=agua,
                luz=luz,
                CO2=co2,
                cat=cat
            )
               
            return JsonResponse({
                "produto": produto.nome, 
                "mensagem": f'Produto "{produto.nome}" inserido com sucesso!'
                }, status=201)
    
        except json.JSONDecodeError:
            return JsonResponse({"erro": "Formato JSON inválido."}, status=400)
    elif request.method == "PUT":
        # alterações
        return HttpResponse("put")
    elif request.method == "DELETE":
        try:
            data = json.loads(request.body)

        # Obter o ID do produto
            id = data.get('id')

        # Buscar produto com base no id
            produto = Produto.objects.filter(id=id).first()

            if not produto:
                return JsonResponse({"erro": "Produto não encontrado."}, status=404)

            produto.delete()

            return JsonResponse({"mensagem": "Produto removido com sucesso!"})

        except json.JSONDecodeError:
            return JsonResponse({"erro": "Formato JSON inválido."}, status=400)

@csrf_exempt
def fornecedor(request):                                                                   
    if request.method == "GET":
        nome=request.GET.get('nome', '').strip().lower()
        local=request.GET.get('local', '').strip()
        categoria=request.GET.get('cat', '').strip()
        id=request.GET.get('id', '').strip()

        f=Fornecedor.objects.all().filter(nome__icontains=nome, local__icontains=local, cat__icontains=categoria, id__icontains=id)

        return JsonResponse({"fornecedor":list(f.values())})
    
    elif request.method == "POST":

        try:
            nome=request.POST.get('nome').strip().capitalize()
            coefAgua=float(request.POST.get('coefAgua', 1))
            coefLuz=float(request.POST.get('coefLuz', 1))
            coefCO2=float(request.POST.get('coefCO2', 1))
            local=request.POST.get('local').strip().capitalize()
            cat=request.POST.get('cat').strip().capitalize()

            if nome and local and cat:

                if Fornecedor.objects.filter(nome=nome).exists():
                    return JsonResponse({"erro": "Fornecedor já existe na Base de Dados!."}, status=400)
                else:
                    fornecedor=Fornecedor.objects.create(
                        nome=nome,
                        coefAgua=coefAgua,
                        coefLuz=coefLuz,
                        coefCO2=coefCO2,
                        local=local,
                        cat=cat
                    )
                        
                    return JsonResponse({ 
                        "mensagem": f'Fornecedor "{fornecedor.nome}" inserido com sucesso!'
                        }, status=201)
        except AttributeError:
            return JsonResponse({"erro": "Faltam parâmetros."}, status=400)
        except ValueError:
            return JsonResponse({"erro": "Valor inválido para coeficientes."}, status=400)
        
    elif request.method == "PUT":

        try:
            # Carregar dados do corpo da requisição
            data = json.loads(request.body)

            # Obter o ID do fornecedor
            id = data.get('id').strip()
        
            fornecedor = Fornecedor.objects.filter(id=id).first()

            if not fornecedor:
                return JsonResponse({"erro": "Fornecedor não encontrado."}, status=404)

            fornecedor.nome = data.get('nome', fornecedor.nome).strip().capitalize()
            fornecedor.coefAgua = float(data.get('coefAgua', fornecedor.coefAgua).strip())
            fornecedor.coefLuz = float(data.get('coefLuz', fornecedor.coefLuz).strip())
            fornecedor.coefCO2 = float(data.get('coefCO2', fornecedor.coefCO2).strip())
            fornecedor.local = data.get('local', fornecedor.local).strip().capitalize()
            fornecedor.cat = data.get('cat', fornecedor.cat).strip()

            fornecedor.save()

            return JsonResponse({"mensagem": f'Fornecedor "{fornecedor.nome}" atualizado com sucesso'})

        except json.JSONDecodeError:
            return JsonResponse({"erro": "Formato JSON inválido."}, status=400)
        except AttributeError:
            return JsonResponse({"erro": "Faltam parâmetros."}, status=400)
        except ValueError:
            return JsonResponse({"erro": "Valor inválido para coeficientes."}, status=400)
        
    elif request.method == "DELETE":
        try:
            data = json.loads(request.body)

            # Obter o ID do fornecedor
            id = data.get('id').strip()

            # Buscar o fornecedor com o ID
            fornecedor = Fornecedor.objects.filter(id=id).first()

            if not fornecedor:
                return JsonResponse({"erro": "Fornecedor não encontrado."}, status=404)

            fornecedor.delete()

            return JsonResponse({"mensagem": f'Fornecedor com id {id} removido com sucesso.'})

        except json.JSONDecodeError:
            return JsonResponse({"erro": "Formato JSON inválido."}, status=400)
        except AttributeError:
            return JsonResponse({"erro": "Faltam parâmetros."}, status=400)


@csrf_exempt
def distribuidor(request):
    if request.method == "GET":

        nome=request.GET.get("nome", "").strip().lower()
        local=request.GET.get("local", "").strip().lower()
        id=request.GET.get("id", "").strip().lower()

        dist=Distribuidor.objects.all().filter(nome__icontains=nome, local__icontains=local, id__icontains=id)

        return JsonResponse({"distribuidor":list(dist.values())})
    
    elif request.method == "POST":
        # create
        if request.POST.get():
            nome=request.POST.get("nome").strip().capitalize()
            local=request.POST.get("local").strip()
            coefluz=request.POST.get("coefluz", "1").strip()
            
            if nome and local:
                if Distribuidor.objects.filter(nome=nome).exists():
                    return JsonResponse({"erro": "Distribuidor já existe na Base de Dados!."}, status=400)
                else:
                    new_d=Distribuidor.objects.create(nome=nome,local=local,coefluz=coefluz)
                    return JsonResponse({
                        "distribuidor": new_d.nome, 
                        "mensagem": f'Distribuidor "{new_d.nome}" inserido com sucesso!'
                        }, status=201)
            
            else:
                return JsonResponse({"erro": "Formato JSON inválido."}, status=400)
            
        else:
            
            return JsonResponse({"erro": "Formato JSON inválido."}, status=400)
        
    elif request.method == "PUT":
        # alterações
        return HttpResponse("put")
    elif request.method == "DELETE":
        # remover
        return HttpResponse("del")

@csrf_exempt
def transportador(request):
    if request.method == "GET":

        nome=request.GET.get("nome", "").strip().lower()
        local=request.GET.get("local", "").strip().lower()
        id=request.GET.get("id", "").strip().lower()

        trans=Transportador.objects.all().filter(nome__icontains=nome, local__icontains=local, id__icontains=id)

        return JsonResponse({"transportador":list(trans.values())})
    
    elif request.method == "POST":
        # create
        return HttpResponse("coisa")
    elif request.method == "PUT":
        # alterações
        return HttpResponse("put")
    elif request.method == "DELETE":
        # remover
        return HttpResponse("del")

def impacto(request):
    pass

def ideal(request):
    pass

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