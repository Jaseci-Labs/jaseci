resource "azurerm_kubernetes_cluster" "zsb_aks" {
  name                = "zsb_aks"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "zsbaks"

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_D2_v2"
    enable_auto_scaling = true
  }

  service_principal {
    client_id     = "00000000-0000-0000-0000-000000000000"
    client_secret = "00000000000000000000000000000000"
  }
}

resource "azurerm_kubernetes_cluster_node_pool" "aks_nood_pool" {
  name                  = "internal"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.zsb_aks.id
  vm_size               = "Standard_DS2_v2"
  node_count            = 1

  tags = {
    Environment = "Production"
  }
}