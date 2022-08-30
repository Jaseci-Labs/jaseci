terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">=2.99.0"
    }

    random = {
      source  = "hashicorp/random"
      version = "3.0.0"
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

# resource "azurerm_kubernetes_cluster" "aks" {
#   name = "zsb_aks"
#   resource_group_name = azurerm_resource_group.rg.name
#   location = azurerm_resource_group.rg.location
#   dns_prefix          = "zsb-aks"


#   default_node_pool {
#     name       = "default"
#     node_count = 1
#     vm_size    = "Standard_D2_v2"
#   }


# }



# resource "azurerm_storage_account" "storage_account" {
#   name = "zsbdevops"
#   resource_group_name = azurerm_resource_group.rg.name
#   location = azurerm_resource_group.rg.location
#   account_tier = "Standard"
#   account_replication_type = "LRS"
# }