import decimal
import json

from botocore.vendored import requests


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
    print("viacep")


# viacep("90480200")


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
    print("postmon")
    # print(consulta)


# postmon("90480200")


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
    print("ws")


# ws("90480200")


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
    print("cepaberto")


# cepaberto("90480200")


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
        return json.loads("{\"erro\": true, \"mensagem\": \"Formato incorreto\"}")
    else:
        print("portalpostal")


# portalpostal("90480200")


def find_cep(cep):
    cep = str(cep).replace("-", "").replace(".", "")
    try:
        viacep(ceap)
    except:
        try:
            postmon(cep)
        except:
            try:
                ws(cep)
            except:
                try:
                    cepaberto(cep)
                except:
                    try:
                        portalpostal(cep)
                    except Exception as e:
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
    print(cep_info)
    return {
        "statusCode": 200,
        "body": json.dumps(cep_info, sort_keys=True,  ensure_ascii=False, indent=4, cls=DecimalEncoder),
    }

# lambda_handler({
#   "queryStringParameters": {
#     "cep": "90480200"
#   }
# },"")