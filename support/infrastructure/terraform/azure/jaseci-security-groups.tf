resource "azurerm_network_security_group" "worker_group_mgmt_one" {
  name = "worker_group_mgmt_one"
  resource_group_name = azurerm_resource_group.rg.name
  location = azurerm_resource_group.rg.location
  
  security_rule {
    name                       = "security_rule_worker_group_mgmt_one"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "22"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "10.0.0.0/8"
  }
}

resource "azurerm_network_security_group" "worker_group_mgmt_two" {
  name = "worker_group_mgmt_two"
  resource_group_name = azurerm_resource_group.rg.name
  location = azurerm_resource_group.rg.location
  
  security_rule {
    name                       = "security_rule_worker_group_mgmt_two"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "22"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "192.168.0.0/16"
  }
}

resource "azurerm_network_security_group" "all_worker_mgmt" {
  name = "all_worker_mgmt"
  resource_group_name = azurerm_resource_group.rg.name
  location = azurerm_resource_group.rg.location
  
  security_rule {
    name                       = "security_rule_all_worker_mgmt"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "22"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"
  }
}