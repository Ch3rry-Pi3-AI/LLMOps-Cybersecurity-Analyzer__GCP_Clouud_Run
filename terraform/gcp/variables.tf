###############################
# Core GCP Settings
###############################

# GCP project where resources will be created
variable "project_id" {
  description = "GCP Project ID."
  type        = string
}

# Region for deploying Cloud Run and Artifact Registry
variable "region" {
  description = "GCP region for Cloud Run deployment."
  type        = string
  default     = "us-central1"
}

# Logical name for the Cloud Run service and Artifact Registry repo
variable "service_name" {
  description = "Name of the Cloud Run service."
  type        = string
  default     = "cyber-analyzer"
}

###############################
# Application Secrets
###############################

# OpenAI API key injected into the container
variable "openai_api_key" {
  description = "OpenAI API key for the application."
  type        = string
  sensitive   = true
  default     = ""
}

# Semgrep App Token for security scanning
variable "semgrep_app_token" {
  description = "Semgrep app token for security scanning."
  type        = string
  sensitive   = true
  default     = ""
}

###############################
# Docker Image Configuration
###############################

# Tag used when building and pushing the Docker image
variable "docker_image_tag" {
  description = "Tag for the Docker image."
  type        = string
  default     = "latest"
}
