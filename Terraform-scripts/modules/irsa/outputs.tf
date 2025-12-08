output "service_account_name" {
  value = kubernetes_service_account.sa.metadata[0].name
}

output "iam_role_arn" {
  value = aws_iam_role.irsa_role.arn
}
