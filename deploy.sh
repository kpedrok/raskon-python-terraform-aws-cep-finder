#/bin/bash

cd terraform
terraform init
terraform plan -out=plan
terraform apply plan
rm plan

# aws apigateway create-deployment --rest-api-id `(cd terraform; terraform output api_id)` --stage-name `(cd terraform; terraform output api_stage_name)`