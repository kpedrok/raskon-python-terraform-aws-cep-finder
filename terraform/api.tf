resource "aws_api_gateway_rest_api" "api" {
  name        = "raskon-cep"
  description = ""
}

resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id = "${aws_api_gateway_rest_api.api.id}"
  stage_name  = "prod"
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
