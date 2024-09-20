terraform {
  backend "s3" {
    bucket = "vehicle-api-terraform-qa"
    region = "eu-west-1"
    key    = "terraform.tfstate"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.66.0"
    }
  }
}

provider "aws" {
  region = "eu-west-1"
  # {...}
}

locals {
  env_vars = {} # ...
}

module "vpc" {
  source = "./modules/vpc"
  # {...}
}

module "docdb" {
  source = "./modules/docdb"

  vpc_security_group_ids = module.vpc.tier3_security_group_ids
  subnet_ids             = module.vpc.tier3_subnets_ids

  cluster_identifier = var.name
}

module "lambda" {
  source = "./modules/lambda"

  vpc_security_group_ids = module.vpc.tier2_security_group_ids
  subnet_ids             = module.vpc.tier2_subnets_ids

  lambda_layer_output_file = "requirements.zip"
  lambda_layer_output_path = "python/"

  env_vars = merge(
    {
      DB_ENDPOINT               = module.docdb.docdb_cluster_endpoint,
      DB_USERNAME_SSM_PARAMETER = module.docdb.docdb_cluster_username_ssm_parameter,
      DB_PASSWORD_SSM_PARAMETER = module.docdb.docdb_cluster_password_ssm_parameter,
      COLLECTION_NAME           = "Vehicles"
    },
    # {...}
  )

  handler       = "handler._handler"
  function_name = var.name
  source_arn    = module.alb.target_group_arn
  principal     = "elasticloadbalancing.amazonaws.com"
  code_dir      = "./api"
  root_dir      = "."
}

module "acm" {
  source = "./modules/acm"

  domain_name = var.domain_name
  zone_name   = var.zone_name
}

module "alb" {
  source = "./modules/alb"

  vpc_security_group_ids = module.vpc.tier1_security_group_ids
  subnet_ids             = module.vpc.tier1_subnets_ids

  certificate_arn = module.acm.certificate_arn

  domain_name = var.domain_name
  zone_name   = var.zone_name

  target_type = "lambda"
  vpc_id      = module.vpc.vpc_id
  name        = var.name
}

module "waf" {
  source = "./modules/waf"


  resource_arns = [module.alb.alb_arn]
  name          = var.name
}

# {...}
