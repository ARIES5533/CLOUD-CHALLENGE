variable "project_name" {
  description = "A unique name for the project, used as a prefix for resources."
  type        = string
  default     = "cloud-challenge"
}

variable "aws_region" {
  description = "The AWS region to deploy resources into."
  type        = string
  default     = "us-east-1"
}

variable "service-account" {
  description = "Service account for EKS"
  type        = string
  default     = "aux-service-sa"
}

variable "namespace" {
  description = "Cluster Namespace for service account creation"
  type        = string
  default     = "aux-service-ns"
}

variable "cluster_name" {
  description = "Cluster name"
  type        = string
  default     = "cloud-challenge"
}
##################################