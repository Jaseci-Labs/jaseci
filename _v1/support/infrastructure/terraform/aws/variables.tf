

variable "development_aws_account_id" {}
variable "development_aws_role_arn" {}
# variable "production_aws_account_id" {}
# variable "production_aws_role_arn" {}


 variable "clusterversion" {}
 variable "instance_type" {}
 variable "instance_type_list" {}
 variable "region" {}


#List only AWS accounts that the script will apply  - environment.auto.tfvars
variable "allowed_account_ids" {
  description = "List of allowed AWS account ids where resources can be created"
  default     = []
}