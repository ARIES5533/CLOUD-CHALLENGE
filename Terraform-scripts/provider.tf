# providers.tf (Root Directory)

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.20"
    }
  }
   
  backend "s3" {
    bucket  = "cloud-challenge-tf-state"
    key     = "backend-config/terraform.tfstate"
    region  = "us-east-1"
    encrypt = true

    ## enable native locking
    use_lockfile = true
  }

}

provider "aws" {
  region = var.aws_region
}
