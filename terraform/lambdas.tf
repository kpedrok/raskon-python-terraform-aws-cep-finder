module "lambda_raskon_cep" {
  source        = "github.com/fernandoruaro/serverless.tf//lambda/api_gateway"
  path          = "../raskon-cep/"
  handler       = "raskon-cep.lambda_handler"
  function_name = "raskon-consulta-cep"
  runtime       = "python3.7"
  timeout       = "5"
}

module "lambda_raskon_ibge" {
  source        = "github.com/fernandoruaro/serverless.tf//lambda/api_gateway"
  path          = "../raskon-ibge/"
  handler       = "raskon-ibge.lambda_handler"
  function_name = "raskon-consulta-ibge"
  runtime       = "python3.7"
  timeout       = "5"
}
