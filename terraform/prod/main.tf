module "vehicle_api" {
  source = "git::https://github.com/dschro-1993/vehicle-api-terraform-module.git?ref=0.1.0"

  openapi_spec_path = "${path.module}/../../openapi.yml"
  code_path         = "${path.module}/../../vehicle_api"
  zone_name         = "292372118261.starfish-rentals.com"
  app_handler       = "api_resolver.lambda_handler"
  app_version       = var.app_version
  env               = "prod"
}
