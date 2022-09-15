# Configure the Microsoft Azure Provider
provider "azurerm" {
  subscription_id = var.subscription_id
  client_id = var.client_id
  tenant_id =  var.tenant_id
  client_secret = var.client_secret

  features {}
}
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "2.39.0"
    }

    local = {
      source  = "hashicorp/local"
      version = "2.0.0"
    }

    null = {
      source  = "hashicorp/null"
      version = "3.0.0"
    }

    template = {
      source  = "hashicorp/template"
      version = "2.2.0"
    }

    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.0.1"
    }
  }
}

resource "azurerm_resource_group" "rg" {
  name     = "${local.resource_group_name}"
  location = "${local.location}"
  tags = {
    "CostCentre" = "ZeroShotBot"
  }
} 
