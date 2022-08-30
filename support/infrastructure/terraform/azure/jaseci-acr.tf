#  ACR

resource "azurerm_container_registry" "zsb-acr" {
  name                = "zsbacr"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = false
}