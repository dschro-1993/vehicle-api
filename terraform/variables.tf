# AWS-Terraform-Provider

variable "region" {
  default = "eu-west-1"
  type    = string
}

variable "tags" {
  type = map(any)
}

# API

variable "root_path" {
  default = ".." # => Jumps 1 level above here!
  type    = string
}

variable "code_path" {
  default = "../vehicle_api"
  type    = string
}

variable "zone_name" {
  default = "292372118261.starfish-rentals.com"
  type    = string
}

variable "lambda_layer_output_file" {
  default = "requirements.zip"
  type    = string
}

variable "lambda_layer_output_path" {
  default = "python"
  type    = string
}

variable "lambda_handler" {
  default = "api_handler.handler"
  type    = string
}

# Todo: Extract from "pyproject.toml"
variable "app_version" {
  default = "0.1.0-rc"
  type    = string
}

variable "app_name" {
  default = "vehicle-api"
  type    = string
}

variable "env_vars" {
  type = map(any)
}

variable "env" {
  type = string
}
