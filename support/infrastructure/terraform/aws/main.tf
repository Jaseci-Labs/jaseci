#For AWS, it is required that the user for prod will have an assume role "terraform-prod-user" for zsb
provider "aws" {
  region              = var.region
  allowed_account_ids = var.allowed_account_ids
  assume_role {
    role_arn = lookup(local.provider_env_roles, local.env)
  }
}

# Activate the comment out section for remote storage of TF state files
terraform {
  # backend "s3" {
  #   bucket = "jaseci-devops"
  #   key    = "dev/"
  #   region = "us-west-2"
  # }

  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "3.0.0"
    }

    local = {
      source  = "hashicorp/local"
      version = "2.0.0"
    }

    null = {
      source  = "hashicorp/null"
      version = "3.0.0"
    }

    template = {
      source  = "hashicorp/template"
      version = "2.2.0"
    }

    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.0.1"
    }
  }
}