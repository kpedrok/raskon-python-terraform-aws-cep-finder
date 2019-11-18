#/bin/bash
export AWS_PROFILE=raskon
export AWS_DEFAULT_REGION='us-east-1'

# aws s3 ls

cd terraform
terraform graph > base.dot
code base.dot
terraform graph | dot -Tsvg > graph.svg
code graph.svg
# terraform init
# terraform plan -out=plan
# terraform apply plan
# rm plan