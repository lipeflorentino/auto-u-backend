variable "project_id" {
  description = "O ID do projeto no GCP"
  type        = string
}

variable "region" {
  description = "Região para o deploy"
  type        = string
  default     = "southamerica-east1"
}

variable "service_name" {
  description = "Nome do serviço no Cloud Run"
  type        = string
  default     = "auto-u-backend"
}

variable "repository_id" {
  description = "Nome do repositório no Artifact Registry"
  type        = string
  default     = "auto-u-repo"
}