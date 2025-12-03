###############################
# Terraform and Providers
###############################

# Core Terraform settings and required provider versions
terraform {
  required_version = ">= 1.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

###############################
# Google Provider Configuration
###############################

# Configure the Google provider with project and region
provider "google" {
  project = var.project_id
  region  = var.region
}

# Fetch client configuration (used for Docker auth access token)
data "google_client_config" "default" {}

###############################
# Enable Required GCP APIs
###############################

# Cloud Run API
resource "google_project_service" "cloudrun" {
  service            = "run.googleapis.com"
  disable_on_destroy = false
}

# Artifact Registry API
resource "google_project_service" "artifactregistry" {
  service            = "artifactregistry.googleapis.com"
  disable_on_destroy = false
}

# Cloud Build API
resource "google_project_service" "cloudbuild" {
  service            = "cloudbuild.googleapis.com"
  disable_on_destroy = false
}

###############################
# Docker Provider & Image Build
###############################

# Configure Docker provider to authenticate against Artifact Registry
provider "docker" {
  registry_auth {
    # Artifact Registry Docker endpoint for the given region
    address  = "${var.region}-docker.pkg.dev"
    # Use OAuth2 access token for authentication
    username = "oauth2accesstoken"
    password = data.google_client_config.default.access_token
  }
}

# Artifact Registry repository for storing Docker images
resource "google_artifact_registry_repository" "app" {
  location      = var.region
  repository_id = var.service_name
  format        = "DOCKER"
  description   = "Docker repository for ${var.service_name}"
}

# Build the application Docker image from the repository root
resource "docker_image" "app" {
  # <region>-docker.pkg.dev/<project>/<repo>/<image>:<tag>
  name = "${var.region}-docker.pkg.dev/${var.project_id}/${var.service_name}/${var.service_name}:${var.docker_image_tag}"

  build {
    # Use the repo root as the build context (two levels up from terraform/gcp)
    context    = "${path.module}/../.."
    dockerfile = "Dockerfile"
    platform   = "linux/amd64"
    no_cache   = true
  }

  depends_on = [
    google_project_service.cloudbuild,
    google_artifact_registry_repository.app,
  ]
}

# Push the built image to Artifact Registry
resource "docker_registry_image" "app" {
  name = docker_image.app.name

  depends_on = [
    google_artifact_registry_repository.app,
    docker_image.app,
  ]
}

###############################
# Cloud Run Deployment
###############################

# Deploy the container image to Cloud Run
resource "google_cloud_run_service" "app" {
  name     = var.service_name
  location = var.region

  template {
    spec {
      containers {
        # Use the image pushed to Artifact Registry
        image = docker_image.app.name

        # Resource limits (2Gi required for Semgrep MCP server)
        resources {
          limits = {
            cpu    = "1"
            memory = "2Gi"
          }
        }

        # Application environment variables
        env {
          name  = "OPENAI_API_KEY"
          value = var.openai_api_key
        }

        env {
          name  = "SEMGREP_APP_TOKEN"
          value = var.semgrep_app_token
        }

        env {
          name  = "ENVIRONMENT"
          value = "production"
        }

        # Ensure Python logs are flushed immediately
        env {
          name  = "PYTHONUNBUFFERED"
          value = "1"
        }

        # Backend container port
        ports {
          container_port = 8000
        }
      }
    }

    metadata {
      annotations = {
        # Scale-to-zero configuration
        "autoscaling.knative.dev/minScale" = "0"
        # Upper bound on instances for cost control
        "autoscaling.knative.dev/maxScale" = "1"
      }
    }
  }

  traffic {
    # Route all traffic to the latest revision
    percent         = 100
    latest_revision = true
  }

  depends_on = [
    google_project_service.cloudrun,
    docker_registry_image.app,
  ]
}

###############################
# IAM: Public Access for Cloud Run
###############################

# Allow unauthenticated (public) access to the Cloud Run service
resource "google_cloud_run_service_iam_member" "public" {
  service  = google_cloud_run_service.app.name
  location = google_cloud_run_service.app.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

###############################
# Outputs
###############################

# Public URL of the Cloud Run service
output "service_url" {
  value       = google_cloud_run_service.app.status[0].url
  description = "URL of the deployed Cloud Run service"
}

# Project ID for reference
output "project_id" {
  value       = var.project_id
  description = "GCP Project ID"
}

# Region for reference
output "region" {
  value       = var.region
  description = "GCP region"
}
