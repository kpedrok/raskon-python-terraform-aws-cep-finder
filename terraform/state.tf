provider "aws" {
  region = "${var.region}"
}


terraform {
  backend "s3" {
    bucket  = "raskon-terraform"
    key     = "raskon-cep2.tfstate"
    region  = "us-east-1"
    encrypt = "true"
  }
}