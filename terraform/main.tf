# terraform apply -var-file=tfvars/{env}/api.tfvars 

module "vehicle_api" {
  source = "git::https://github.com/dschro-1993/vehicle-api-terraform-module.git?ref=0.1.0"

  root                     = var.root
  zone_name                = var.zone_name
  code_path                = var.code_path
  requirements_upload_file = var.requirements_upload_file
  requirements_output_path = var.requirements_output_path
  environment_variables    = var.environment_variables
  app_lambda_resolver      = var.app_lambda_resolver
  app_version              = var.app_version
  app_name                 = var.app_name
  env                      = var.env
}
