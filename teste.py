import requests
import json
teste_cep =[
  "01311-300",
  "64056-460",
  "30320-700",
  "41830-520",
  "24070-170",
  "32143-170",
  "58052-310",
  "42829-742",
  "60325-580",
  "90650-070",
  "31260-110",
  "75140-480",
  "60430-560",
  "95780-000",
  "90420-020",
  "39803-171",
  "13569-270",
  "20920-400",
  "01230-010",
  "03579-170",
  "22775-036",
  "49030-210",
  "88138-300",
  "13253-395",
  "68515-000",
  "41940-210",
  "33400-000",
  "80320-040",
  "28925-572",
  "96400-420",
  "02841-090",
  "72405-560",
  "80710-250",
  "70686-060",
  "04671-260",
  "89031-000",
  "66080-680",
  "22250-040",
  "96020-390",
  "15601-242",
  "70876-550",
  "05016-081",
  "31535-400",
  "13087-773",
  "38700-543",
  "38240-000",
  "05351-015",
  "74460-190",
  "89900-000",
  "85015-390",
  "79970-000",
  "01432-010",
  "22280-080",
  "37500-193",
  "74453-330",
  "29904-520",
  "03131-020",
  "40450-211",
  "11065-410",
  "23060-210"
]

for ceps in teste_cep: 
    print(ceps)
    cep = ceps
    url = "https://7lpmbl6zch.execute-api.us-east-1.amazonaws.com/prod/cep?cep=" + cep
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
    print(consulta,"\n")


