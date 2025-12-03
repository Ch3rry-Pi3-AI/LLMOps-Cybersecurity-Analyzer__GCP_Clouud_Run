###############################
# Terraform and Providers
###############################

# Core Terraform settings and required provider versions
terraform {
  required_version = ">= 1.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

# AzureRM provider configuration (features block required, even if empty)
provider "azurerm" {
  features {}
}

###############################
# Naming and Resource Group
###############################

# Random suffix to ensure the ACR name is globally unique
resource "random_string" "acr_suffix" {
  length  = 6
  upper   = false
  lower   = true
  numeric = true
  special = false
}

# Local values for constructing a valid, unique ACR name
locals {
  # Strip hyphens to keep the name alphanumeric
  acr_basename = replace(var.project_name, "-", "")

  # Truncate base name so base + 6-char suffix stays under Azure's 50-char limit
  acr_name = "${substr(local.acr_basename, 0, 40)}${random_string.acr_suffix.result}"
}

# Use an existing resource group rather than creating a new one
data "azurerm_resource_group" "main" {
  name = var.resource_group_name
}

###############################
# Azure Container Registry (ACR)
###############################

# Container registry to store and serve the application Docker image
resource "azurerm_container_registry" "acr" {
  name                = local.acr_name
  resource_group_name = data.azurerm_resource_group.main.name
  location            = data.azurerm_resource_group.main.location
  sku                 = "Basic"
  admin_enabled       = true

  tags = {
    environment = terraform.workspace
    project     = var.project_name
  }
}

###############################
# Docker Provider & Image Build
###############################

# Configure Docker provider to authenticate against the created ACR
provider "docker" {
  registry_auth {
    # ACR login server address
    address = azurerm_container_registry.acr.login_server
    # ACR admin credentials
    username = azurerm_container_registry.acr.admin_username
    password = azurerm_container_registry.acr.admin_password
  }
}

# Build the application Docker image from the repository root
resource "docker_image" "app" {
  # Fully-qualified image name: <acr>/<project>:<tag>
  name = "${azurerm_container_registry.acr.login_server}/${var.project_name}:${var.docker_image_tag}"

  build {
    # Use the repo root as the build context (two levels up from terraform/azure)
    context    = "${path.module}/../.."
    dockerfile = "Dockerfile"
    platform   = "linux/amd64"
    no_cache   = true
  }
}

# Push the built image to ACR
resource "docker_registry_image" "app" {
  name = docker_image.app.name

  # Ensure the image is built before pushing
  depends_on = [docker_image.app]
}

###############################
# Monitoring: Log Analytics
###############################

# Log Analytics workspace used by Azure Container Apps for monitoring and logs
resource "azurerm_log_analytics_workspace" "main" {
  name                = "${var.project_name}-logs"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30

  tags = {
    environment = terraform.workspace
    project     = var.project_name
  }
}

###############################
# Container Apps Environment
###############################

# Azure Container App Environment (shared infrastructure for container apps)
resource "azurerm_container_app_environment" "main" {
  name                       = "${var.project_name}-env"
  location                   = data.azurerm_resource_group.main.location
  resource_group_name        = data.azurerm_resource_group.main.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id

  tags = {
    environment = terraform.workspace
    project     = var.project_name
  }
}

###############################
# Container App (Application)
###############################

# Main containerised application definition for Azure Container Apps
resource "azurerm_container_app" "main" {
  name                         = var.project_name
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = data.azurerm_resource_group.main.name
  revision_mode                = "Single"

  # Container runtime configuration
  template {
    container {
      name   = "main"
      image  = docker_registry_image.app.name
      cpu    = 1.0
      memory = "2.0Gi"

      # OpenAI API key (injected as an environment variable)
      env {
        name  = "OPENAI_API_KEY"
        value = var.openai_api_key
      }

      # Semgrep App Token used for security scanning
      env {
        name  = "SEMGREP_APP_TOKEN"
        value = var.semgrep_app_token
      }

      # Application environment marker used by the backend
      env {
        name  = "ENVIRONMENT"
        value = "production"
      }

      # Ensure Python output is unbuffered for clearer logs
      env {
        name  = "PYTHONUNBUFFERED"
        value = "1"
      }
    }

    # Scale-to-zero and maximum single replica for cost control
    min_replicas = 0
    max_replicas = 1
  }

  # Public ingress configuration
  ingress {
    external_enabled = true
    target_port      = 8000

    # Route 100% of traffic to the latest revision
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  # Registry credentials configuration for pulling images from ACR
  registry {
    server              = azurerm_container_registry.acr.login_server
    username            = azurerm_container_registry.acr.admin_username
    password_secret_name = "registry-password"
  }

  # Secret holding the ACR password, referenced above
  secret {
    name  = "registry-password"
    value = azurerm_container_registry.acr.admin_password
  }

  tags = {
    environment = terraform.workspace
    project     = var.project_name
  }
}

###############################
# Outputs
###############################

# Public URL of the deployed application
output "app_url" {
  value       = "https://${azurerm_container_app.main.ingress[0].fqdn}"
  description = "URL of the deployed application"
}

# ACR login server used for pushing/pulling images
output "acr_login_server" {
  value       = azurerm_container_registry.acr.login_server
  description = "Azure Container Registry login server"
}

# Resource group used for all Azure resources
output "resource_group" {
  value       = data.azurerm_resource_group.main.name
  description = "Resource group name"
}
