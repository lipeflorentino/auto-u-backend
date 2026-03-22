# 1. Repositório para as imagens Docker
resource "google_artifact_registry_repository" "backend_repo" {
  location      = var.region
  repository_id = var.repository_id
  description   = "Repositorio Docker para o Auto-U Backend"
  format        = "DOCKER"

  cleanup_policies {
    id     = "delete-old-images"
    action = "DELETE"
    condition {
      older_than = "2592000s"
    }
  }

  cleanup_policies {
    id     = "keep-latest-versions"
    action = "KEEP"
    most_recent_versions {
      keep_count = 3
    }
  }
}

# 2. Serviço Cloud Run
resource "google_cloud_run_v2_service" "backend_service" {
  name     = var.service_name
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    scaling {
      min_instance_count = 0
      max_instance_count = 3
    }
    containers {
      # Imagem temporária (será atualizada pelo GitHub Actions)
      image = "us-docker.pkg.dev/cloudrun/container/hello" 
      
      resources {
        limits = {
          cpu    = "2"
          memory = "2Gi"
        }
        cpu_idle = true
      }
      
      env {
        name  = "CLOUD_PROVIDER"
        value = "gcp"
      }

      env {
        name  = "HUGGINGFACE_TOKEN"
        value = var.huggingface_token 
      }

      env {
        name  = "STAGE"
        value = "production"
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