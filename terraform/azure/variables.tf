###############################
# Core Project Settings
###############################

# Logical name for this application / deployment
variable "project_name" {
  description = "Name of the project (used for resource naming)."
  type        = string
  default     = "cyber-analyzer"
}

# Azure region to deploy resources into (kept for flexibility if needed later)
variable "location" {
  description = "Azure region for resources."
  type        = string
  default     = "eastus"
}

# Existing resource group where all resources will be created
variable "resource_group_name" {
  description = "Name of the resource group."
  type        = string
  default     = "cyber-analyzer-rg"
}

###############################
# Application Secrets
###############################

# OpenAI API key injected into the container as an environment variable
variable "openai_api_key" {
  description = "OpenAI API key for the application."
  type        = string
  sensitive   = true
  default     = ""
}

# Semgrep App Token injected for security scanning tooling
variable "semgrep_app_token" {
  description = "Semgrep app token for security scanning."
  type        = string
  sensitive   = true
  default     = ""
}

###############################
# Docker Image Configuration
###############################

# Tag applied to the built Docker image (e.g. latest, v1.0.0)
variable "docker_image_tag" {
  description = "Tag for the Docker image."
  type        = string
  default     = "latest"
}
