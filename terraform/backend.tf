# Backend Configuration for Remote State (Optional)
# 
# To use remote state storage, uncomment and configure this backend.
# This is recommended for production environments.
#
# Prerequisites:
# 1. Create an Azure Storage Account
# 2. Create a container named "tfstate"
# 3. Update the values below
#
# terraform {
#   backend "azurerm" {
#     resource_group_name  = "rg-terraform-state"
#     storage_account_name = "your-unique-storage-account"
#     container_name       = "tfstate"
#     key                  = "karel-agent.terraform.tfstate"
#   }
# }

# Uncomment the lines below if you want to use local state with encryption
# terraform {
#   required_version = ">= 1.0"
#   required_providers {
#     azurerm = {
#       source  = "hashicorp/azurerm"
#       version = "~> 3.0"
#     }
#   }
# }