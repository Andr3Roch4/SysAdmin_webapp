from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Produto, Distribuidor, Fornecedor, Transportador
from .helpers import calcular_recursos, impact_score, cadeia_menor_impact
from django.core import serializers
import csv
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

@csrf_exempt
def produto(request):

    if request.method == "GET":
        nome=request.GET.get('nome', '').strip().lower()
        categoria=request.GET.get('cat', '').strip()
        id=request.GET.get('id', '')
        p=Produto.objects.all().filter(nome__icontains=nome, cat__icontains=categoria, id__icontains=id)
        return JsonResponse({"produto":list(p.values())})
    
    elif request.method == "POST":
        try:
            nome=request.POST.get('nome').strip().capitalize()
            peso_carregamento=int(request.POST.get('peso_carregamento')) 
            agua=int(request.POST.get('agua')) 
            luz=int(request.POST.get('luz'))
            co2=int(request.POST.get('co2'))
            cat=request.POST.get('cat').strip().capitalize()
            if Produto.objects.filter(nome__iexact=nome).exists():
                return JsonResponse({"erro": "Produto já existe na Base de Dados!."}, status=400)   
            produto=Produto.objects.create(
                nome=nome,
                peso_carregamento=peso_carregamento,
                agua=agua,
                luz=luz,
                CO2=co2,
                cat=cat
            )  
            return JsonResponse({
                "mensagem": f"Produto '{produto.nome}' inserido com sucesso!"
                }, status=201)
        except AttributeError:
            return JsonResponse({"erro": "Faltam parâmetros."}, status=400)
        except ValueError:
            return JsonResponse({"erro": "Valor inválido."}, status=400)
        
    elif request.method == "PUT":       
        try:
            data = json.loads(request.body)                             # Carregar dados do corpo da requisição
            id = data.get('id')                                         # Obter o ID
            produto = Produto.objects.filter(id=id).first()
            if not produto:
                return JsonResponse({"erro": "Produto não encontrado."}, status=404)
            else:
                produto.nome = data.get('nome', produto.nome).strip().capitalize()
                produto.peso_carregamento = int(data.get('peso_carregamento', produto.peso_carregamento))
                produto.agua = int(data.get('agua', produto.agua))
                produto.luz = int(data.get('luz', produto.luz))
                produto.CO2 = int(data.get('CO2', produto.CO2))
                produto.cat = data.get('cat', produto.cat).strip().capitalize()
                produto.save()
                return JsonResponse({"mensagem": f'Produto "{produto.nome}" atualizado com sucesso'})
        except json.JSONDecodeError:
            return JsonResponse({"erro": "Formato JSON inválido."}, status=400)
        except AttributeError:
            return JsonResponse({"erro": "Faltam parâmetros."}, status=400)
        except ValueError:
            return JsonResponse({"erro": "Valor inválido."}, status=400)

    elif request.method == "DELETE":
        try:
            data = json.loads(request.body)
            id = data.get('id')                                         # Obter o ID do produto
            produto = Produto.objects.filter(id=id).first()             # Buscar produto com base no id
            if not produto:
                return JsonResponse({"erro": "Produto não encontrado."}, status=404)
            else:
                produto.delete()
                return JsonResponse({"mensagem": f'Produto com id {id} removido com sucesso.'})
        except json.JSONDecodeError:
            return JsonResponse({"erro": "Formato JSON inválido."}, status=400)
        except AttributeError:
            return JsonResponse({"erro": "Faltam parâmetros."}, status=400)
        except ValueError:
            return JsonResponse({"erro": "Valor inválido."}, status=400)

@csrf_exempt
def fornecedor(request):                                                                   
    if request.method == "GET":
        nome=request.GET.get('nome', '').strip().lower()
        local=request.GET.get('local', '').strip()
        categoria=request.GET.get('cat', '').strip()
        id=request.GET.get('id', '')
        f=Fornecedor.objects.all().filter(nome__icontains=nome, local__icontains=local, cat__icontains=categoria, id__icontains=id)
        return JsonResponse({"fornecedor":list(f.values())})
    
    elif request.method == "POST":
        try:
            nome=request.POST.get('nome').strip().capitalize()
            coefAgua=float(request.POST.get('coefagua', 1))
            coefLuz=float(request.POST.get('coefluz', 1))
            coefCO2=float(request.POST.get('coefco2', 1))
            local=request.POST.get('local').strip().capitalize()
            cat=request.POST.get('cat').strip().capitalize()
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
            return JsonResponse({"erro": "Valor inválido."}, status=400)
        
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)                             # Carregar dados do corpo da requisição
            id = data.get('id')                                         # Obter o ID do fornecedor
            fornecedor = Fornecedor.objects.filter(id=id).first()
            if not fornecedor:
                return JsonResponse({"erro": "Fornecedor não encontrado."}, status=404)
            else:
                fornecedor.nome = data.get('nome', fornecedor.nome).strip().capitalize()
                fornecedor.coefAgua = float(data.get('coefagua', fornecedor.coefAgua))
                fornecedor.coefLuz = float(data.get('coefluz', fornecedor.coefLuz))
                fornecedor.coefCO2 = float(data.get('coefco2', fornecedor.coefCO2))
                fornecedor.local = data.get('local', fornecedor.local).strip().capitalize()
                fornecedor.cat = data.get('cat', fornecedor.cat).strip().capitalize()
                fornecedor.save()
                return JsonResponse({"mensagem": f"Fornecedor '{fornecedor.nome}' atualizado com sucesso"})
        except json.JSONDecodeError:
            return JsonResponse({"erro": "Formato JSON inválido."}, status=400)
        except AttributeError:
            return JsonResponse({"erro": "Faltam parâmetros."}, status=400)
        except ValueError:
            return JsonResponse({"erro": "Valor inválido."}, status=400)
        
    elif request.method == "DELETE":
        try:
            data = json.loads(request.body)
            id = data.get('id')                                             # Obter o ID do fornecedor
            fornecedor = Fornecedor.objects.filter(id=id).first()           # Buscar o fornecedor com o ID
            if not fornecedor:
                return JsonResponse({"erro": "Fornecedor não encontrado."}, status=404)
            else:
                fornecedor.delete()
                return JsonResponse({"mensagem": f'Fornecedor com id {id} removido com sucesso.'})
        except json.JSONDecodeError:
            return JsonResponse({"erro": "Formato JSON inválido."}, status=400)
        except AttributeError:
            return JsonResponse({"erro": "Faltam parâmetros."}, status=400)
        except ValueError:
            return JsonResponse({"erro": "Valor inválido."}, status=400)

@csrf_exempt
def distribuidor(request):
    if request.method == "GET":
        nome=request.GET.get("nome", "").strip().lower()
        local=request.GET.get("local", "").strip().lower()
        id=request.GET.get("id", "")
        dist=Distribuidor.objects.all().filter(nome__icontains=nome, local__icontains=local, id__icontains=id)
        return JsonResponse({"distribuidor":list(dist.values())})
    
    elif request.method == "POST":
        try:
            nome=request.POST.get("nome").strip().capitalize()
            local=request.POST.get("local").strip().capitalize()
            coefluz=float(request.POST.get("coefluz", 1))
            if Distribuidor.objects.filter(nome=nome).exists():
                return JsonResponse({"erro": "Distribuidor já existe na Base de Dados!."}, status=400)
            else:
                new_d=Distribuidor.objects.create(nome=nome,local=local,coefLuz=coefluz)
                return JsonResponse({
                    "mensagem": f'Distribuidor "{new_d.nome}" inserido com sucesso!'
                    }, status=201)
        except AttributeError:
            return JsonResponse({"erro": "Faltam parâmetros."}, status=400)
        except ValueError:
            return JsonResponse({"erro": "Valor inválido."}, status=400)
        
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)                                 # Carregar dados do corpo da requisição
            id = data.get('id')                                             # Obter o ID do distribuidor
            d = Distribuidor.objects.filter(id=id).first()
            if not d:
                return JsonResponse({"erro": "Distribuidor não encontrado."}, status=404)
            else:
                d.nome = data.get('nome', d.nome).strip().capitalize()
                d.local = data.get('local', d.local).strip().capitalize()
                d.coefLuz = float(data.get('coefluz', d.coefLuz))
                d.save()
                return JsonResponse({"mensagem": f'Distribuidor "{d.nome}" atualizado com sucesso'})
        except json.JSONDecodeError:
            return JsonResponse({"erro": "Formato JSON inválido."}, status=400)
        except AttributeError:
            return JsonResponse({"erro": "Faltam parâmetros."}, status=400)
        except ValueError:
            return JsonResponse({"erro": "Valor inválido."}, status=400)
        
    elif request.method == "DELETE":
        try:
            data = json.loads(request.body)
            id = data.get('id')                                             # Obter o ID do distribuidor
            d = Distribuidor.objects.filter(id=id).first()                  # Buscar o distribuidor com o ID
            if not d:
                return JsonResponse({"erro": "Distribuidor não encontrado."}, status=404)
            else:
                d.delete()
                return JsonResponse({"mensagem": f'Distribuidor com id {id} removido com sucesso.'})
        except json.JSONDecodeError:
            return JsonResponse({"erro": "Formato JSON inválido."}, status=400)
        except AttributeError:
            return JsonResponse({"erro": "Faltam parâmetros."}, status=400)
        except ValueError:
            return JsonResponse({"erro": "Valor inválido."}, status=400)

@csrf_exempt
def transportador(request):
    if request.method == "GET":
        nome=request.GET.get("nome", "").strip().lower()
        local=request.GET.get("local", "").strip().lower()
        id=request.GET.get("id", "")
        t=Transportador.objects.all().filter(nome__icontains=nome, local__icontains=local, id__icontains=id)
        return JsonResponse({"transportador":list(t.values())})
    
    elif request.method == "POST":
        try:
            nome=request.POST.get("nome").strip().capitalize()
            local=request.POST.get("local").strip().capitalize()
            coefluz=float(request.POST.get("coefluz", 1))
            coefCO2=float(request.POST.get("coefco2", 1))
            if Transportador.objects.filter(nome=nome).exists():
                return JsonResponse({"erro": "Transportador já existe na Base de Dados!."}, status=400)
            else:
                new_t=Transportador.objects.create(nome=nome,local=local,coefLuz=coefluz,coefCO2=coefCO2)
                return JsonResponse({
                    "mensagem": f'Transportador "{new_t.nome}" inserido com sucesso!'
                    }, status=201)
        except AttributeError:
            return JsonResponse({"erro": "Faltam parâmetros."}, status=400)
        except ValueError:
            return JsonResponse({"erro": "Valor inválido."}, status=400)
        
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)                             # Carregar dados do corpo da requisição
            id = data.get('id')                                         # Obter o ID do transportador
            t = Transportador.objects.filter(id=id).first()
            if not t:
                return JsonResponse({"erro": "Transportador não encontrado."}, status=404)
            else:
                t.nome = data.get('nome', t.nome).strip().capitalize()
                t.local = data.get('local', t.local).strip().capitalize()
                t.coefLuz = float(data.get('coefluz', t.coefLuz))
                t.coefCO2 = float(data.get('coefco2', t.coefLuz))
                t.save()
                return JsonResponse({"mensagem": f'Transportador "{t.nome}" atualizado com sucesso'})
        except json.JSONDecodeError:
            return JsonResponse({"erro": "Formato JSON inválido."}, status=400)
        except AttributeError:
            return JsonResponse({"erro": "Faltam parâmetros."}, status=400)
        except ValueError:
            return JsonResponse({"erro": "Valor inválido."}, status=400)
        
    elif request.method == "DELETE":
        try:
            data = json.loads(request.body)
            id = data.get('id')                                         # Obter o ID do transportador
            t = Transportador.objects.filter(id=id).first()             # Buscar o transportador com o ID
            if not t:
                return JsonResponse({"erro": "Transportador não encontrado."}, status=404)
            else:
                t.delete()
                return JsonResponse({"mensagem": f'Transportador com id {id} removido com sucesso.'})
        except json.JSONDecodeError:
            return JsonResponse({"erro": "Formato JSON inválido."}, status=400)
        except AttributeError:
            return JsonResponse({"erro": "Faltam parâmetros."}, status=400)
        except ValueError:
            return JsonResponse({"erro": "Valor inválido."}, status=400)

@csrf_exempt
def impacto(request):
    if request.method == "POST":
        try:
            # recebe 4 parametros sempre
            id_p=request.POST.get("produto")
            id_d=request.POST.get("distribuidor")
            id_f=request.POST.get("fornecedor")
            id_t=request.POST.get("transportador")
            p=Produto.objects.get(id=id_p)
            d=Distribuidor.objects.get(id=id_d)
            f=Fornecedor.objects.get(id=id_f)
            t=Transportador.objects.get(id=id_t)
            # calcula o impacto 
            agua_cadeia, luz_cadeia, co2_cadeia=calcular_recursos(p,d,f,t)
            score=impact_score(agua_cadeia, luz_cadeia, co2_cadeia)
            # retorna json com informaçao da cadeia escolhida e luz+co2+agua gastos e score do impacto
            json_return={
                "produto":f"{p.nome}",
                "fornecedor":f"{f.nome}, {f.local}",
                "distribuidor":f"{d.nome}, {d.local}",
                "transportador":f"{t.nome}, {t.local}",
                f"luz kWh por kg de {p.nome}":f"{luz_cadeia:.2f}",
                f"co2 kg CO2 por kg de {p.nome}":f"{co2_cadeia:.2f}",
                f"agua litros por kg de {p.nome}":f"{agua_cadeia:.2f}",
                "score":f"{score:.2f}"
            }
            return JsonResponse(json_return)
        except AttributeError:
            return JsonResponse({"erro": "Faltam parâmetros."}, status=400)
        except ValueError:
            return JsonResponse({"erro": "Valor inválido."}, status=400)

@csrf_exempt
def ideal(request):
    if request.method == "POST":
        try:
            # recebe 2 parametros sempre
            id_p=request.POST.get("produto")
            id_d=request.POST.get("distribuidor")
            p=Produto.objects.get(id=id_p)
            d=Distribuidor.objects.get(id=id_d)
            # calcula cadeia mais eficiente
            dict_escolhas=cadeia_menor_impact(p, d)
            f=dict_escolhas["fornecedor"]
            t=dict_escolhas["transportador"]
            luz=dict_escolhas["luz_cadeia"]
            co2=dict_escolhas["co2_cadeia"]
            agua=dict_escolhas["agua_cadeia"]
            score=dict_escolhas["score"]
            # retorna json com informaçao da cadeia mais eficiente e luz+co2+agua gastos e score do impacto
            json_return={
                "produto":f"{p.nome}",
                "fornecedor":f"{f.nome}, {f.local}",
                "distribuidor":f"{d.nome}, {d.local}",
                "transportador":f"{t.nome}, {t.local}",
                f"luz kWh por kg de {p.nome}":f"{luz:.2f}",
                f"co2 kg CO2 por kg de {p.nome}":f"{co2:.2f}",
                f"agua litros por kg de {p.nome}":f"{agua:.2f}",
                "score":f"{score:.2f}"
            }
            return JsonResponse(json_return)
        except AttributeError:
            return JsonResponse({"erro": "Faltam parâmetros."}, status=400)
        except ValueError:
            return JsonResponse({"erro": "Valor inválido."}, status=400)


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