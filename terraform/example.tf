provider "aws" {
  region = "us-east-1"
}

module "lambda_query_cep" {
  source        = "github.com/fernandoruaro/serverless.tf//lambda/api_gateway"
  path          = "../consulta-cep/"
  handler       = "consulta_cep.lambda_handler"
  function_name = "teste-consulta-cep"
  runtime       = "python3.7"
  timeout       = 300

  extra_policy_statements = [<<EOF
{
  "Effect": "Allow",
  "Action": "dynamodb:*",
  "Resource": "*"
}
EOF
  ]
}

# module "query_cep" {
#   source      = "github.com/fernandoruaro/serverless.tf//api_gateway/resource"
#   rest_api_id = "${aws_api_gateway_rest_api.api.id}"
#   parent_id   = "${aws_api_gateway_rest_api.api.root_resource_id}"
#   path_part   = "query-cep"
# }

# module "query_cep_get" {
#   source              = "github.com/fernandoruaro/serverless.tf//api_gateway/method/lambda"
#   rest_api_id         = "${aws_api_gateway_rest_api.api.id}"
#   resource_id         = "${aws_api_gateway_rest_api.query_cep.id}"
#   http_request_method = "GET"

#   lambda_invoke_arn = "${module.lambda_query_cep.lambda_invoke_arn}"
# }

# resource "aws_api_gateway_rest_api" "MyDemoAPI" {
#   name        = "MyDemoAPI"
#   description = "This is my API for demonstration purposes"
# }


# resource "aws_api_gateway_resource" "MyDemoResource" {
#   rest_api_id = "${aws_api_gateway_rest_api.MyDemoAPI.id}"
#   parent_id   = "${aws_api_gateway_rest_api.MyDemoAPI.root_resource_id}"
#   path_part   = "test"
# }


# resource "aws_api_gateway_method" "MyDemoMethod" {
#   rest_api_id   = "${aws_api_gateway_rest_api.MyDemoAPI.id}"
#   resource_id   = "${aws_api_gateway_rest_api.MyDemoResource.id}"
#   http_method   = "GET"
#   authorization = "NONE"
# }


# resource "aws_api_gateway_integration" "MyDemoIntegration" {
#   rest_api_id = "${aws_api_gateway_rest_api.MyDemoAPI.id}"
#   resource_id = "${aws_api_gateway_resource.MyDemoResource.id}"
#   http_method = "${aws_api_gateway_method.MyDemoMethod.http_method}"
#   type        = "MOCK"
# }


# resource "aws_api_gateway_deployment" "MyDemoDeployment" {
#   depends_on = ["aws_api_gateway_integration.MyDemoIntegration"]


#   rest_api_id = "${aws_api_gateway_rest_api.MyDemoAPI.id}"
#   stage_name  = "test"


#   variables = {
#     "answer" = "42"
#   }
# }

