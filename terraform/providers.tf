terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.66.0"
    }
  }
}

provider "aws" {
  # {...}
  # assume_role {
  #   role_arn     = "arn:aws:iam::{account-id}:role/{role-name}"
  #   session_name = "terraform-session"
  #   duration     = 900
  # }
  default_tags { tags = var.tags }
  region = var.region
  # {...}
}
