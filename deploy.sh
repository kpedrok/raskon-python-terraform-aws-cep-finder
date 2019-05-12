#/bin/bash
cd terraform
terraform init
terraform plan -out=plan
terraform apply plan
rm plan