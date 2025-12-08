variable "cluster_name" {
  type = string
}

variable "namespace" {
  type = string
}

variable "service_account_name" {
  type = string
}

variable "iam_role_name" {
  type    = string
  default = "aux-service-irsa-role"
}

variable "policy_name" {
  type    = string
  default = "aux-service-policy"
}
