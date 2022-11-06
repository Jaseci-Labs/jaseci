
# Create AWS EKS Infrastructure for Jaseci using Terraform #

## Preparation #

1) Make sure you have a valid AWS Account
2) Create Access Key and Secret with EKS, Ec2 , VPC , IAm permissions
3) Connect your local computer to aws using AWS CLI (using AWS Configure)
4) Install terraform CLI from https://www.terraform.io/downloads
4) Update the config.tf file with respective key values as described
5) Update environment.auto.tfvars file with your AWS Account Id and related configuiration of cluster as needed.

## Initilaize ##

Run below commoand to initialize your terraform

```bash

Terraform init

```

## Plan - To check if all Configuration is properly Set ##

```bash
Terraform plan
```
## Apply - Get Set Go, Create jaseci Cluster  ##

```bash
Terraform apply
```

## Destroy - if you need to delete the infrastructure, you can use below command  ##

```bash
Terraform destroy
```

## NOTE  ##

By default terraform runs on default workspace which adds dev environment to the cluster suffix. If you want to create multiple environment , for example prod , add Prod related values in config.tf

Workspace can be created and switched using below command

```bash
terraform workspace new <environment-Name>
```

or you can select when you want to run updates on any environmnet using 

```bash
terraform workspace select <environment-Name>
```

