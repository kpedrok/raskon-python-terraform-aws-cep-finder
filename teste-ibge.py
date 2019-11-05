import requests
import json
url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios/"

headers = {
    'User-Agent': "PostmanRuntime/7.19.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "46cab9e1-fa41-43fa-95a6-4cb78287ef8a,2f2afc54-c954-4f02-a042-0bf5206fe27f",
    'Host': "servicodados.ibge.gov.br",
    'Accept-Encoding': "gzip, deflate",
    'Cookie': "ROUTEID=.sdadosSSL2",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
}

response = requests.request("GET", url, headers=headers)


lista_ibge = response.text
lista_ibge = json.loads(lista_ibge)
i = 0
for linha in lista_ibge:
    i = i+1
    print(i," - ", linha['microrregiao']['mesorregiao']['UF']['sigla'], " - ", linha['nome'], " - ",linha['id'])
