import decimal
# import requests
from botocore.vendored import requests
import json
from unicodedata import normalize
import os

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

cep_info = {}

def find_ibge(uf,cidade):
    with open('ibge.json', encoding='utf-8-sig') as codigos_ibge:
        codigos_ibge = json.load(codigos_ibge)
        for cod in codigos_ibge:
            chave = str(formatar_texto(str(uf+cidade)))
            chave_json = formatar_texto(cod['Chave'])
            if  chave_json == chave:
                return (cod['IBGE'])

def viacep(cep):
    cep = cep
    url = 'https://viacep.com.br/ws/' + cep + '/json/'
    consulta = json.loads(requests.get(url).text)
    cep_info['cep'] = consulta['cep']
    cep_info['logradouro'] = consulta['logradouro']
    cep_info['numero'] = consulta['complemento']
    cep_info['bairro'] = consulta['bairro']
    cep_info['cidade'] = consulta['localidade']
    cep_info['uf'] = consulta['uf']
    cep_info['ibge'] = consulta['ibge']
    print("viacep", consulta, "\n")

def postmon(cep):
    cep = cep
    url = "http://api.postmon.com.br/v1/cep/" + cep
    consulta = json.loads(requests.get(url).text)
    cep_info['cep'] = consulta['cep']
    cep_info['logradouro'] = consulta['logradouro']
    cep_info['numero'] = consulta['complemento']
    cep_info['bairro'] = consulta['bairro']
    cep_info['cidade'] = consulta['cidade']
    cep_info['uf'] = consulta['estado']
    cep_info['ibge'] = consulta['cidade_info']['codigo_ibge']
    print("postmon", consulta, "\n")

def ws(cep):
    cep = cep
    url = "http://ws.matheuscastiglioni.com.br/ws/cep/find/" + cep + "/json"
    consulta = json.loads(requests.get(url).text)
    cep_info['cep'] = consulta['cep']
    cep_info['logradouro'] = consulta['logradouro']
    cep_info['numero'] = consulta['complemento']
    cep_info['bairro'] = consulta['bairro']
    cep_info['cidade'] = consulta['cidade']
    cep_info['uf'] = consulta['estado']
    cep_info['ibge'] = consulta['codibge']
    print("ws", consulta, "\n")

def cepaberto(cep):
    cep = cep
    url = "http://www.cepaberto.com/api/v3/cep"
    querystring = {"cep": cep}
    headers = {'authorization': "Token token=0e317139c2550a618d7c0eb40eaaf854"}
    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    consulta = json.loads(response.text)
    cep_info['cep'] = consulta['cep']
    cep_info['logradouro'] = consulta["logradouro"].split(",")[0]
    cep_info['numero'] = consulta["logradouro"].split(", ")[1]
    cep_info['bairro'] = consulta['bairro']
    cep_info['cidade'] = consulta['cidade']['nome']
    cep_info['uf'] = consulta['estado']['sigla']
    cep_info['ibge'] = consulta['cidade']['ibge']
    print("cepaberto", consulta, "\n")

def portalpostal(cep):
    cep = cep
    url = "http://www.portalpostal.com.br/rest/secure/cep/" + cep
    headers = {
        'pragma': "no-cache",
        'login': "taglivros",
        'authorization': "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0YWdsaXZyb3MiLCJyb2xlcyI6InVzZXIiLCJpYXQiOjE1NTc0MjA2MDB9.Nncdxz3TnbBytesB9qcIUUvBkFXJTRtS6TGWzHVWqgQ",
        'empresa.cnpj': "97095772000196",
        'accept': "application/json, text/plain, */*",
        'idusuario': "1465",
        'cache-control': "no-cache",
        'idcliente': "10086",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
    }
    response = requests.request("GET", url, headers=headers)
    consulta = json.loads(response.text)
    print(consulta)
    cep_info['cep'] = consulta['data']['endereco']['cep']
    cep_info['logradouro'] = consulta['data']['endereco']['logradouro']
    cep_info['numero'] = ""
    cep_info['bairro'] = consulta['data']['endereco']['bairro']
    cep_info['cidade'] = consulta['data']['endereco']['cidade']
    cep_info['uf'] = consulta['data']['endereco']['uf']
    cep_info['ibge'] = ""
    if cep_info['logradouro'] == 'CEP inexistente':
        print("Erro - ", cep)
        cep_info['logradouro'] = ""
        # return json.loads("{\"erro\": true, \"mensagem\": \"Formato incorreto\"}")
        return {
            "statusCode": 400,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.loads("{\"erro\": true, \"mensagem\": \"Formato incorreto\"}"),
        }
    else:
        print("portalpostal", consulta, "\n")

def cepla (cep):
        url = "http://cep.la/" + cep
        headers = {
            'cache-control': "no-cache",
            'Accept': "application/json",
            }
        response = requests.request("GET", url, headers=headers)
        consulta = json.loads(response.text)
        cep_info['cep'] = consulta['cep']
        cep_info['logradouro'] = consulta["logradouro"].split("-")[0]
        cep_info['numero'] = ''
        cep_info['bairro'] = consulta['bairro']
        cep_info['cidade'] = consulta['cidade']
        cep_info['uf'] = consulta['uf']
        uf = formatar_texto(cep_info['uf'])
        cidade = formatar_texto(cep_info['cidade'])
        cep_info['ibge'] = str(find_ibge(uf,cidade))
        print("cepla", consulta, "\n")

def formatar_texto(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII').strip().lower().replace(" ", "-")

def find_cep(cep):
    cep = str(cep).replace("-", "").replace(".", "")
    try:
        viacep(cep)

    except:
        try:
            postmon(cep)
        except:
            try:
                cepaberto(cep)
            except:
                try:
                    ws(cep)
                except:
                        cepla(cep)

    cep_info['cep'] = str(cep_info['cep'])
    cep_info['logradouro'] = str(cep_info['logradouro'].title())
    cep_info['numero'] = str(cep_info['numero'].title())
    cep_info['bairro'] = str(cep_info['bairro'].title())
    cep_info['cidade'] = str(cep_info['cidade'].title())
    cep_info['uf'] = str(cep_info['uf'].upper())
    cep_info['ibge'] = str(cep_info['ibge'])

def lambda_handler(event, context):
    input_cep = str(event['queryStringParameters']['cep'])
    try:
        find_cep(event['queryStringParameters']['cep'])
        print(json.dumps(cep_info, sort_keys=True,
                        ensure_ascii=False, indent=2, cls=DecimalEncoder))
        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            "body": json.dumps(cep_info, sort_keys=True,  ensure_ascii=False, indent=2, cls=DecimalEncoder),
        }
    except Exception as e:
        print("CEP: ", input_cep, "Erro: ", e)
        return {
            "statusCode": 400,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": ("CEP: ", input_cep, "Erro: ", e),
        }

# lambda_handler({
#     "queryStringParameters": {
#         "cep": "2fdf9904-520"
#     }
# }, "")

# cep = '29904-520'
# cep = '76868-000'
# cepla(cep)
# viacep(cep)
# postmon(cep)
# ws(cep)
# cepaberto(cep)
# portalpostal(cep)