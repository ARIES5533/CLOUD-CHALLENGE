# providers.tf

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
    bucket  = ""
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


provider "kubernetes" {
  host                   = data.aws_eks_cluster.eks.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.eks.certificate_authority[0].data)
  token                  = data.aws_eks_cluster_auth.eks.token
}
