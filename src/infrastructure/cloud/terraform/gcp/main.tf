# 1. Repositório para as imagens Docker
resource "google_artifact_registry_repository" "backend_repo" {
  location      = var.region
  repository_id = var.repository_id
  description   = "Repositorio Docker para o Auto-U Backend"
  format        = "DOCKER"
}

# 2. Serviço Cloud Run
resource "google_cloud_run_v2_service" "backend_service" {
  name     = var.service_name
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      # Imagem temporária (será atualizada pelo GitHub Actions)
      image = "us-docker.pkg.dev/cloudrun/container/hello" 
      
      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
      
      env {
        name  = "CLOUD_PROVIDER"
        value = "gcp"
      }
    }
  }
  
  lifecycle {
    ignore_changes = [
      template[0].containers[0].image, 
    ]
  }
}

# 3. Permissão para acesso não autenticado (Público)
resource "google_cloud_run_v2_service_iam_binding" "public_access" {
  name     = google_cloud_run_v2_service.backend_service.name
  location = google_cloud_run_v2_service.backend_service.location
  role     = "roles/run.invoker"
  members  = ["allUsers"]
}