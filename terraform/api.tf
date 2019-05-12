resource "aws_api_gateway_rest_api" "api" {
  name        = "raskon-cep1"
  description = ""
}

resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id = "${aws_api_gateway_rest_api.api.id}"
  stage_name = "master"
}

module "raskon_cep_path" {
  source      = "github.com/fernandoruaro/serverless.tf//api_gateway/resource"
  rest_api_id = "${aws_api_gateway_rest_api.api.id}"
  parent_id   = "${aws_api_gateway_rest_api.api.root_resource_id}"
  path_part   = "raskon_cep2"
}

module "raskon_cep_path_get" {
  source      = "github.com/fernandoruaro/serverless.tf//api_gateway/method/lambda"
  rest_api_id = "${aws_api_gateway_rest_api.api.id}"
  resource_id   = "${module.raskon_cep_path.id}"
  http_request_method = "GET"
  lambda_invoke_arn = "${module.lambda_raskon_cep.lambda_invoke_arn}"
}