# All Configs variables assigned  here
allowed_account_ids = ["12345678"] # Add you Azure Account ID in comma separated list. You can add multiple account Ids here


#Dev Environment settings (default workspace)
development_azure_account_id = "12345678" # Add you Azure Account ID
development_azure_role_arn   = ""

# #Prod Environment setting (production workspace)  #when you craete Prod Environment uncomment this

# production_azure_account_id = ""
# production_azure_role_arn   = ""




resource_group_name = "${local.productprefix}-infra"
location = "eastus"
cluster_name        = "${local.productprefix}-aks"
