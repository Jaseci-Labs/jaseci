
#Common Tags - environment.auto.tfvars
variable "department" {}
variable "cost_centre" {}
variable "product_owner" {}
variable "product_manager" {}
variable "portfolio_manager" {}
variable "product_name" {}
variable "managed_by" {}

#Default RDS password - environment.auto.tfvars
# variable "default_rds_password" {}

variable "development_aws_account_id" {}
variable "development_aws_role_arn" {}
# variable "production_aws_account_id" {}
# variable "production_aws_role_arn" {}

variable "subnet-ids" {
  default = [
      "172.20.0.0/24",
      "172.20.16.0/24",
      "172.20.32.0/24"
  ]
}

#List only AWS accounts that the script will apply  - environment.auto.tfvars
variable "allowed_account_ids" {
  description = "List of allowed AWS account ids where resources can be created"
  //type        = tolist([any])
  default     = []
}