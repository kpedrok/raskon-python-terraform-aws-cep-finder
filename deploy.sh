#/bin/bash

# export AWS_ACCESS_KEY_ID=AKIAIU4PND4LOG4TSHHQ
# export AWS_SECRET_ACCESS_KEY=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
cd terraform
terraform init
terraform plan -out=plan
terraform apply plan
rm plan

# aws apigateway create-deployment --rest-api-id `(cd terraform; terraform output api_id)` --stage-name `(cd terraform; terraform output api_stage_name)`