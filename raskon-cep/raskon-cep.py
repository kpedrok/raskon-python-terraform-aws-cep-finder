import decimal
# import requests
from botocore.vendored import requests
import json
from unicodedata import normalize


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


cep_info = {}


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
    try:
        url = "http://cep.la/" + cep
        headers = {
            'cache-control': "no-cache",
            'Accept': "application/json",
            }

        response = requests.request("GET", url, headers=headers)
        consulta = json.loads(response.text)
        cep_info['cep'] = consulta['cep']
        cep_info['logradouro'] = consulta["logradouro"].split("-")[0]
        cep_info['numero'] = ' '
        cep_info['bairro'] = consulta['bairro']
        cep_info['cidade'] = consulta['cidade']
        cep_info['uf'] = consulta['uf']
        uf = formatar_texto(cep_info['uf'])
        cidade = formatar_texto(cep_info['cidade'])
        url = "https://cidades.ibge.gov.br/brasil/" + uf + "/" + cidade + "/panorama"
        response_ibge = requests.request("GET", url)
        ibge = response_ibge.text
        ibge = (ibge.split('Código do Município'))[1].split('Gentílico')[0].strip()
        ibge = (ibge.split('class="topo__valor">')
                )[1].split('</p>')[0].strip()
        cep_info['ibge'] = str(ibge)
        print("cepla", consulta, "\n")
    except:
        print("Erro - ", cep)
        return {
            "statusCode": 400,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.loads("{\"erro\": true, \"mensagem\": \"Formato incorreto\"}"),
        }

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
                    try:
                        cepla(cep)
                    except Exception as e:
                        print("erro")
                        print(e)
                        return json.loads("{\"erro\": true, \"mensagem\": \"Formato incorreto\"}")

    cep_info['cep'] = str(cep_info['cep'])
    cep_info['logradouro'] = str(cep_info['logradouro'].title())
    cep_info['numero'] = str(cep_info['numero'].title())
    cep_info['bairro'] = str(cep_info['bairro'].title())
    cep_info['cidade'] = str(cep_info['cidade'].title())
    cep_info['uf'] = str(cep_info['uf'].upper())
    cep_info['ibge'] = str(cep_info['ibge'])


def lambda_handler(event, context):
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

# lambda_handler({
#     "queryStringParameters": {
#         "cep": "29904520"
#     }
# }, "")

# cep = '29904-520'
# cep = '04180-112aaa'
# cepla(cep)
# viacep(cep)
# postmon(cep)
# ws(cep)
# cepaberto(cep)
# portalpostal(cep)


# erros= ['24070-170',]

# teste_cep =[
#   "01311-300",
#   "64056-460",
#   "30320-700",
#   "41830-520",
#   "24070-170",
#   "32143-170",
#   "58052-310",
#   "42829-742",
#   "60325-580",
#   "90650-070",
#   "31260-110",
#   "75140-480",
#   "60430-560",
#   "95780-000",
#   "90420-020",
#   "39803-171",
#   "13569-270",
#   "20920-400",
#   "01230-010",
#   "03579-170",
#   "22775-036",
#   "49030-210",
#   "88138-300",
#   "13253-395",
#   "68515-000",
#   "41940-210",
#   "33400-000",
#   "80320-040",
#   "28925-572",
#   "96400-420",
#   "02841-090",
#   "72405-560",
#   "80710-250",
#   "70686-060",
#   "04671-260",
#   "89031-000",
#   "66080-680",
#   "22250-040",
#   "96020-390",
#   "15601-242",
#   "70876-550",
#   "05016-081",
#   "31535-400",
#   "13087-773",
#   "38700-543",
#   "38240-000",
#   "05351-015",
#   "74460-190",
#   "89900-000",
#   "85015-390",
#   "79970-000",
#   "01432-010",
#   "22280-080",
#   "37500-193",
#   "74453-330",
#   "29904-520",
#   "03131-020",
#   "40450-211",
#   "11065-410",
#   "23060-210"
# ]

# for ceps in teste_cep:
#     print(ceps)
#     lambda_handler({
#     "queryStringParameters": {
#         "cep":ceps
#     }
# }, "")
