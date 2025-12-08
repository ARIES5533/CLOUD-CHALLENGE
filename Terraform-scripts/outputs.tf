

output "main_api_bucket_name" {
  description = "Name of the S3 bucket for the Main API."
  value       = module.aux_service_storage.bucket_id
}

output "parameter_store_path" {
  description = "The base path for parameters in SSM Parameter Store."
  value       = module.ssm.parameter_store_path
}