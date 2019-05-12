module "lambda_raskon_cep1" {
  source = "github.com/fernandoruaro/serverless.tf//lambda/api_gateway"
  path="../raskon-cep/"
  handler="raskon-cep.lambda_handler"
  function_name="raskon-consulta-cep"
  runtime="python3.7"
  timeout="5"

  extra_policy_statements = [<<EOF
{
  "Effect": "Allow",
  "Action": "dynamodb:*",
  "Resource": "*"
}
EOF
  ]
}
