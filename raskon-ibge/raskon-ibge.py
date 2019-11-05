

import decimal
import json
from unicodedata import normalize
import os
# import requests
from botocore.vendored import requests


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def find_ibge(uf, cidade):
    with open('ibge.json', encoding='utf-8-sig') as codigos_ibge:
        codigos_ibge = json.load(codigos_ibge)
        for cod in codigos_ibge:
            chave = str(formatar_texto(str(uf+cidade)))
            chave_json = formatar_texto(cod['Chave'])
            if chave_json == chave:
                return (cod['IBGE'])


def formatar_texto(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII').strip().lower().replace(" ", "-")


def buscar_ibge(uf, cidade):
    global ibge
    uf = formatar_texto(uf)
    cidade = formatar_texto(cidade)
    url = "https://cidades.ibge.gov.br/brasil/" + uf + "/" + cidade + "/panorama"

    response = requests.request("GET", url)
    ibge = response.text
    ibge = (ibge.split('Código do Município'))[1].split('Gentílico')[0].strip()
    ibge = (ibge.split('class="topo__valor">')
            )[1].split('</p>')[0].strip()
    return (ibge)


def servicos_ibge(uf, cidade):
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios/"

    response = requests.request("GET", url)

    lista_ibge = response.text
    lista_ibge = json.loads(lista_ibge)

    for linha in lista_ibge:
        if formatar_texto(uf) == formatar_texto(linha['microrregiao']['mesorregiao']['UF']['sigla']) and formatar_texto(cidade) == formatar_texto(linha['nome']):
            # print(uf,cidade)
            # print(linha['id'], linha['nome'],linha['microrregiao']['mesorregiao']['UF']['sigla'])
            return (linha['id'])


def lambda_handler(event, context):
    print('buscar_ibge')
    try:
        ibge = buscar_ibge(event['queryStringParameters']['uf'],
                           event['queryStringParameters']['cidade'])
        print(1, ibge)
        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(ibge, sort_keys=True,  ensure_ascii=False, indent=2, cls=DecimalEncoder),
        }

    except:
        print('find_ibge')
        try:
            ibge = find_ibge(event['queryStringParameters']['uf'],
                             event['queryStringParameters']['cidade'])
            print(2, ibge)
            if ibge == None:
                raise ValueError('find_ibge didnt work')

            return {
                "statusCode": 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                },
                "body": json.dumps(ibge, sort_keys=True,  ensure_ascii=False, indent=2, cls=DecimalEncoder), }
        except:
            print('servicos_ibge')
            try:
                ibge = servicos_ibge(event['queryStringParameters']['uf'],
                                     event['queryStringParameters']['cidade'])
                print(3, ibge)
               
                return {
                    "statusCode": 200,
                    'headers': {
                        'Access-Control-Allow-Origin': '*'
                    },
                    "body": json.dumps(ibge, sort_keys=True,  ensure_ascii=False, indent=2, cls=DecimalEncoder),
                }

            except Exception as e:
                print(e)
                return {
                    "statusCode": 400,
                    'headers': {
                        'Access-Control-Allow-Origin': '*'
                    },
                    "body": json.dumps(e, sort_keys=True,  ensure_ascii=False, indent=2, cls=DecimalEncoder),
                }


# lambda_handler({
#     "queryStringParameters": {
#         "uf": "SP",
#         "cidade": "Carapicuíba"
#     }
# }, "")
