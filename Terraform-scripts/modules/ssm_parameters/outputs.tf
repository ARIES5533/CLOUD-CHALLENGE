output "parameter_store_path" {
  description = "The base path created for parameters in SSM Parameter Store."
  value       = "/${var.project_name}/"
}

output "read_arn_prefix" {
  description = "ARN prefix for read permissions to be used in IAM policy."
  value       = "arn:aws:ssm:${var.region}:${data.aws_caller_identity.current.account_id}:parameter/${var.project_name}/*"
}

data "aws_caller_identity" "current" {}