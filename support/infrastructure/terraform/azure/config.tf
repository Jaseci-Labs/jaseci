locals {
  env           = terraform.workspace
  productprefix = "jaseci"

  #Name Variables
  resource_group_name = "jaseci-infra"
  location = "eastus2"
  cluster_name = "jaseci-aks"

  #BEGIN: Workspace Environments (index is based on workspace selected)
  environments = {
    "default"    = "Development"
    "production" = "Production"
  }

  envs = {
    "default"    = "dev"
    "production" = "prod"
  }

  #Local Variables 
  environment = lookup(local.environments, local.env)
  envprefix   = lookup(local.envs, local.env)
  envsuffix   = lookup(local.envs, local.env)
  stdprefix   = "${local.productprefix}-${local.envprefix}"



  #Boolean Variables
  isProd = local.env == "production" ? 1 : 0
  isDev  = local.env == "default" ? 1 : 0

 
}