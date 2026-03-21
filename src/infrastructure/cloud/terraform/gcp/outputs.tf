output "service_url" {
  description = "A URL gerada para acessar o backend no Cloud Run"
  value       = google_cloud_run_v2_service.backend_service.uri
}

output "artifact_registry_repo" {
  description = "O caminho completo do repositório de imagens"
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${var.repository_id}"
}

output "project_id" {
  description = "O ID do projeto utilizado"
  value       = var.project_id
}