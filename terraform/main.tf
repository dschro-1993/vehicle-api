# terraform apply -var-file=tfvars/{env}/api.tfvars 

module "vehicle_api" {
  source = "git::https://github.com/dschro-1993/vehicle-api-terraform-module.git?ref=0.2.0-rc"

  root_path = var.root_path
  code_path = var.code_path

  zone_name = var.zone_name

  lambda_layer_output_file = var.lambda_layer_output_file
  lambda_layer_output_path = var.lambda_layer_output_path

  lambda_handler = var.lambda_handler

  app_version = var.app_version
  app_name    = var.app_name

  env_vars = var.env_vars

  env = var.env
}

# {...}
