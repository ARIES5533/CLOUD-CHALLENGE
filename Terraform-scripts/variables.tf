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
  description = "The AWS region to deploy resources into."
  type        = string
  default     = "aux-service-sa"
}

variable "namespace" {
  description = "The AWS region to deploy resources into."
  type        = string
  default     = "aux-service-ns"
}

variable "cluster_name" {
  description = "The AWS region to deploy resources into."
  type        = string
  default     = "cloud-challenge-cluster"
}
##################################