variable "project_name" {
  description = "The base path for the SSM parameters (e.g., /project_name/)."
  type        = string
}

variable "region" {
  description = "AWS region for ARN construction."
  type        = string
}