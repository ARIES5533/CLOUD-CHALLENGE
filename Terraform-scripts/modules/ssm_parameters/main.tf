# Define the root path for better organization
locals {
  path = "/${var.project_name}"
}

resource "aws_ssm_parameter" "api_version" {
  name  = "${local.path}/main-api-version"
  type  = "String"
  value = "v1.0.0"
}

resource "aws_ssm_parameter" "aux_version" {
  name  = "${local.path}/auxiliary-service-version"
  type  = "String"
  value = "v1.0.0"
}

resource "aws_ssm_parameter" "config_key" {
  name  = "${local.path}/secret-key-example"
  type  = "SecureString" # Best practice for secrets
  value = "this-is-a-secret-value-for-the-challenge"
}