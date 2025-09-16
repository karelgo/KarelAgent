variable "resource_group_name" {
  description = "Name of the Azure Resource Group"
  type        = string
  default     = "rg-karel-agent"
}

variable "location" {
  description = "Azure region where resources will be created"
  type        = string
  default     = "East US"
}

variable "app_name" {
  description = "Name of the Azure Web App (must be globally unique)"
  type        = string
}

variable "app_service_sku" {
  description = "SKU for the App Service Plan"
  type        = string
  default     = "B1"

  validation {
    condition = contains([
      "F1", "D1",             # Free/Shared
      "B1", "B2", "B3",       # Basic
      "S1", "S2", "S3",       # Standard
      "P1", "P2", "P3",       # Premium
      "P1v2", "P2v2", "P3v2", # Premium v2
      "P1v3", "P2v3", "P3v3"  # Premium v3
    ], var.app_service_sku)
    error_message = "App Service SKU must be a valid Azure App Service plan SKU."
  }
}

variable "enable_staging_slot" {
  description = "Whether to create a staging deployment slot"
  type        = bool
  default     = false
}

variable "tags" {
  description = "A map of tags to assign to the resources"
  type        = map(string)
  default = {
    Environment = "Production"
    Project     = "KarelAgent"
    ManagedBy   = "Terraform"
  }
}

variable "python_version" {
  description = "Python version for the web app"
  type        = string
  default     = "3.11"

  validation {
    condition = contains([
      "3.8", "3.9", "3.10", "3.11", "3.12"
    ], var.python_version)
    error_message = "Python version must be a supported Azure Web App Python version."
  }
}