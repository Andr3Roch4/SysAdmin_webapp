from geopy import distance
from .models import Produto, Fornecedor, Distribuidor, Transportador
from django.http import HttpResponse, JsonResponse
import random

def calcular_recursos(produto, distribuidor, fornecedor, transportador):
    # Constantes
    luz_distribuidor=1.5        # kWh/24h por kg de produto
    CO2_transportador=0.3       # kg de CO2/km em media dos camioes
    luz_transportador=0.03      # kWh/km em media dos camioes para refrigeração
    tempoarmazenamento=random.randrange(1,30)
    
    distancia_provisoria=float(distancia(fornecedor.local, distribuidor.local))+float(distancia(transportador.local,fornecedor.local))
    if distancia_provisoria < 50:
        distancia_provisoria=50
    #distribuidor.coefs(luz_distribuidor, tempoarmazenamento)
    #fornecedor.coefs(produto.luz, produto.CO2, produto.agua)
    #transportador.coefs(CO2_transportador, luz_transportador, distancia_provisoria, produto.peso_carregamento)
    luz_dist=distribuidor.coefLuz*luz_distribuidor*tempoarmazenamento
    luz_forn=fornecedor.coefLuz*produto.luz
    agua_forn=fornecedor.coefAgua*produto.agua
    co2_forn=fornecedor.coefCO2*produto.CO2
    co2_trans=((transportador.coefCO2*CO2_transportador)*distancia_provisoria)/produto.peso_carregamento
    luz_trans=((transportador.coefLuz*luz_transportador)*distancia_provisoria)/produto.peso_carregamento
    agua_cadeia=agua_forn
    luz_cadeia=luz_dist+luz_forn+luz_trans
    co2_cadeia=co2_forn+co2_trans
    print(agua_cadeia,luz_cadeia,co2_cadeia)
    return agua_cadeia, luz_cadeia, co2_cadeia


# Função para calcular um score ambiental para cada cadeia logísitica. 
def impact_score(aguaCadeia, luzCadeia, CO2Cadeia):           # O score varia de [0-inf[ e scores inferiores refletem menores impactes ambientais
    luzFossil= 0.29*luzCadeia                                 # "produção de renováveis abastece 71% do consumo de eletricidade em 2024" (Portugal)- REN. 1-0.71 = 0.29
    CO2_luz= 0.7*luzFossil                                    # O valor médio para as fontes fósseis em geral fica entre 0,4 a 1,0 kg de CO₂ por kWh gerado. Média = 0.7
    CO2_total= CO2_luz + CO2Cadeia
    score= 0.2*aguaCadeia + 0.8*CO2_total
    return score


def cadeia_menor_impact(produto, distribuidor):
    
    # Listar possiveis fornecedores
    lista_fornecedores_possiveis=[]
    forn_all=Fornecedor.objects.all()
    trans_all=Transportador.objects.all()
    for i in forn_all:
        if produto.cat in i.cat:
            lista_fornecedores_possiveis.append(i)
    
    # Calcular a cadeia ideal com menor impacto
    impact=10000
    fornecedor_escolhido=Fornecedor.objects.all().first()
    transportador_escolhido=Transportador.objects.all().first()
    if not lista_fornecedores_possiveis:
        return JsonResponse({"erro":"Não existe fornecedor para o produto selecionado."}, status=404)
    for f in lista_fornecedores_possiveis:
        for t in trans_all:
            agua_cadeia_provisorio, luz_cadeia_provisorio, co2_cadeia_provisorio=calcular_recursos(produto, distribuidor, f, t)
            impact_provisorio=impact_score(agua_cadeia_provisorio, luz_cadeia_provisorio, co2_cadeia_provisorio)
            if impact > impact_provisorio:
                # Variaveis com info da cadeia escolhida e da que ficou em segundo lugar
                fornecedor_anterior=fornecedor_escolhido
                transportador_anterior=transportador_escolhido
                impact_anterior=impact
                fornecedor_escolhido=f
                transportador_escolhido=t
                impact=impact_provisorio
                agua_cadeia=agua_cadeia_provisorio
                luz_cadeia=luz_cadeia_provisorio
                co2_cadeia=co2_cadeia_provisorio

    return {"fornecedor":fornecedor_escolhido, "transportador":transportador_escolhido, "agua_cadeia":agua_cadeia, "luz_cadeia":luz_cadeia, "co2_cadeia":co2_cadeia, "score":impact}

def distancia(citie1, citie2):
    # Dicionario com latitudes e longitudes
    cidades_portuguesas = {
    "Lisboa": {"latitude": 38.7169, "longitude": -9.1395},
    "Porto": {"latitude": 41.1579, "longitude": -8.6291},
    "Coimbra": {"latitude": 40.2136, "longitude": -8.4265},
    "Braga": {"latitude": 41.5483, "longitude": -8.4294},
    "Aveiro": {"latitude": 40.6413, "longitude": -8.6538},
    "Funchal": {"latitude": 32.6669, "longitude": -16.9265},
    "Ponta Delgada": {"latitude": 37.7412, "longitude": -25.6722},
    "Evora": {"latitude": 38.5669, "longitude": -7.9071},
    "Viseu": {"latitude": 40.6612, "longitude": -7.9122},
    "Albufeira": {"latitude": 37.0137, "longitude": -7.8530},
    "Cascais": {"latitude": 38.6975, "longitude": -9.4213},
    "Sintra": {"latitude": 38.7983, "longitude": -9.3737},
    "Leiria": {"latitude": 39.7431, "longitude": -8.8077},
    "Guimaraes": {"latitude": 41.4475, "longitude": -8.6110},
    "Amadora": {"latitude": 38.7617, "longitude": -9.2315},
    "Setubal": {"latitude": 38.5246, "longitude": -8.8882},
    "Alcobaca": {"latitude": 39.6028, "longitude": -8.9775},
    "Figueira da Foz": {"latitude": 40.1500, "longitude": -8.8667},
    "Braganca": {"latitude": 41.8032, "longitude": -6.7580},
    "Castelo Branco": {"latitude": 39.8233, "longitude": -7.4997},
    "Beja": {"latitude": 38.0156, "longitude": -7.8699},
    "Santarem": {"latitude": 39.2333, "longitude": -8.6850},
    "Barcelos": {"latitude": 41.5305, "longitude": -8.6117},
    "Viana do Castelo": {"latitude": 41.6932, "longitude": -8.8294},
    "Vila Real": {"latitude": 41.3003, "longitude": -7.7401},
    "Povoa de Varzim": {"latitude": 41.3794, "longitude": -8.7803},
    "Oeiras": {"latitude": 38.6939, "longitude": -9.2998},
    "Montijo": {"latitude": 38.6451, "longitude": -8.9757},
    "Tavira": {"latitude": 37.5716, "longitude": -7.6053},
    "Braga": {"latitude": 41.5483, "longitude": -8.4294},
    "Aljustrel": {"latitude": 37.7864, "longitude": -8.1500},
    "Coruche": {"latitude": 38.9019, "longitude": -8.6877},
    "Portalegre": {"latitude": 39.2969, "longitude": -7.4293},
    "Sines": {"latitude": 37.9504, "longitude": -8.8697},
    "Olhao": {"latitude": 37.1407, "longitude": -7.8520},
    "Lagos": {"latitude": 37.1020, "longitude": -8.6744},
    "Celorico da Beira": {"latitude": 40.5295, "longitude": -7.4812},
    "Vila do Conde": {"latitude": 41.3689, "longitude": -8.7479},
    "Lamego": {"latitude": 41.1281, "longitude": -7.8041},
    "Paredes": {"latitude": 41.2370, "longitude": -8.2886},
    "Felgueiras": {"latitude": 41.3736, "longitude": -8.3009},
    "Ovar": {"latitude": 40.9053, "longitude": -8.6110},
    "Santa Maria da Feira": {"latitude": 40.9128, "longitude": -8.5105},
    "Ribeira Grande": {"latitude": 37.8324, "longitude": -25.4329},
    "Sao Joao da Madeira": {"latitude": 40.8641, "longitude": -8.4531},
    "Famalicao": {"latitude": 41.3782, "longitude": -8.5417},
    "Faro": {"latitude": 37.0194, "longitude": -7.9304},
    "Loule": {"latitude": 37.1393, "longitude": -8.0246},
    "Odivelas": {"latitude": 38.7975, "longitude": -9.1703},
    "Vila Nova de Gaia": {"latitude": 41.1331, "longitude": -8.6110},
    "Portimao":{"latitude": 37.1366, "longitude": -8.5377}
    }

    for c in cidades_portuguesas:
        if citie1.lower() == c.lower():
            loc1=c
        elif citie2.lower() == c.lower():
            loc2=c
    if citie1.lower() == citie2.lower():
        loc2=loc1
    try:
        loc1
        loc2
    except NameError:
        print(citie1, citie2)
        print("Não existe uma das cidades na base de dados.")    
        return
    # Calculo da distancia através da lat e long
    location1=(cidades_portuguesas[loc1]["latitude"], cidades_portuguesas[loc1]["longitude"])
    location2=(cidades_portuguesas[loc2]["latitude"], cidades_portuguesas[loc2]["longitude"])
    dist=distance.distance(location1, location2).km
    # retorna a distancia em KM
    return format(dist, ".2f")



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