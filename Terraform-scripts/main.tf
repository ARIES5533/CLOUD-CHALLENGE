
data "aws_eks_cluster" "eks" {
  name = var.cluster_name
}


data "aws_eks_cluster_auth" "eks" {
  name = var.cluster_name
}


module "ssm" {
  source       = "./modules/ssm_parameters"
  project_name = var.project_name
  region       = var.aws_region
}


module "aux_service_storage" {
  source       = "./modules/s3_storage"
  bucket_name  = "cloud-challenge-bucket5533"
  project_name = var.project_name
}




module "aux_api_irsa" {
  source = "./modules/irsa"

  cluster_name         = var.cluster_name
  namespace            = var.namespace
  service_account_name = var.service-account
}
