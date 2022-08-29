terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">=2.99.0"
    }
  }
}
# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "zsbinfra"
  location = "eastus"
  tags = {
        "CostCentre": "ZeroShotBot",
        "Business Owner": "Asim Salim",
        "Technical": "Ashish A"
    }
}