output "grafana_access_key_id" {
  value = aws_iam_access_key.grafana.id
}

output "grafana_secret_access_key" {
  value     = aws_iam_access_key.grafana.secret
  sensitive = true
}