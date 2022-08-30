locals {
  env           = terraform.workspace
  productprefix = "jaseci"


  #BEGIN: Workspace Environments (index is based on workspace selected)
  environments = {
    "default"    = "Development"
    "production" = "Production"
  }

  envs = {
    "default"    = "dev"
    "production" = "prod"
  }

  accountids = {
    "default"    = var.development_aws_account_id
   # "production" = var.production_aws_account_id
  }
  #END: Workspace Environments

  #Local Variables 
  environment = lookup(local.environments, local.env)
  envprefix   = lookup(local.envs, local.env)
  envsuffix   = lookup(local.envs, local.env)
  accountid   = lookup(local.accountids, local.env)
  stdprefix   = "${local.productprefix}-${local.envprefix}"



  #Boolean Variables
  isProd = local.env == "production" ? 1 : 0
  isDev  = local.env == "default" ? 1 : 0



  provider_env_roles = {
    "default"    = var.development_aws_role_arn
    # "production" = var.production_aws_role_arn
  }
}
