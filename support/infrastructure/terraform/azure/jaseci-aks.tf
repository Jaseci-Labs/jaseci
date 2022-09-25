resource "azurerm_kubernetes_cluster" "aks" {
  name                = "${local.cluster_name}"
  kubernetes_version  = "1.24.3"
  location            = "${local.location}"
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "${local.cluster_name}"

  default_node_pool {
    name                = "system"
    node_count          = 2
    vm_size             = "Standard_DS2_v2"
    type                = "VirtualMachineScaleSets"
    availability_zones  = [1, 2, 3]
    enable_auto_scaling = false
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    load_balancer_sku = "Standard"
    network_plugin    = "kubenet" 
  }
}