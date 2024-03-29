resource "aws_api_gateway_rest_api" "api" {
  name        = "raskon-cep"
  description = "API para Consulta de cep"
}

resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id       = "${aws_api_gateway_rest_api.api.id}"
  stage_name        = "prod"
  stage_description = "${md5(file("api.tf"))}"             #Forçar atualização do stage
}

module "raskon_cep" {
  source      = "github.com/fernandoruaro/serverless.tf//api_gateway/resource"
  rest_api_id = "${aws_api_gateway_rest_api.api.id}"
  parent_id   = "${aws_api_gateway_rest_api.api.root_resource_id}"
  path_part   = "cep"
}

module "raskon_cep_get" {
  source              = "github.com/fernandoruaro/serverless.tf//api_gateway/method/lambda"
  rest_api_id         = "${aws_api_gateway_rest_api.api.id}"
  resource_id         = "${module.raskon_cep.id}"
  http_request_method = "GET"
  lambda_invoke_arn   = "${module.lambda_raskon_cep.lambda_invoke_arn}"
}


module "raskon_ibge" {
  source      = "github.com/fernandoruaro/serverless.tf//api_gateway/resource"
  rest_api_id = "${aws_api_gateway_rest_api.api.id}"
  parent_id   = "${aws_api_gateway_rest_api.api.root_resource_id}"
  path_part   = "ibge"
}

module "raskon_ibge_get" {
  source              = "github.com/fernandoruaro/serverless.tf//api_gateway/method/lambda"
  rest_api_id         = "${aws_api_gateway_rest_api.api.id}"
  resource_id         = "${module.raskon_ibge.id}"
  http_request_method = "GET"
  lambda_invoke_arn   = "${module.lambda_raskon_ibge.lambda_invoke_arn}"
}
