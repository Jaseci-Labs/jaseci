
variable "development_azure_account_id" {} 
variable "development_azure_role_arn" {}     
# variable "production_azure_account_id" {}
# variable "production_azure_role_arn" {}

variable "resource_group_name" {
  type        = string
  description = "Resource group name in Azure"
}
variable "location" {
  type        = string
  description = "Resources location in Azure"
}
variable "cluster_name" {
  type        = string
  description = "AKS name in Azure"
}

#List only Azure accounts that the script will apply  - environment.auto.tfvars
variable "allowed_account_ids" {
  description = "List of allowed Azure account ids where resources can be created"
  //type        = tolist([any])
  default     = []
}
