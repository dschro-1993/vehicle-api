# AWS-Provider

variable "default_tags" {
  type = map(any)
}

# API

variable "environment_variables" {
  type = map(any)
}

variable "root" {
  default = ".." # => Jumps one-level up here!
  type    = string
}

variable "requirements_upload_file" {
  default = "requirements.zip"
  type    = string
}

variable "requirements_output_path" {
  default = "python"
  type    = string
}

variable "zone_name" {
  default = "292372118261.starfish-rentals.com"
  type    = string
}

variable "code_path" {
  default = "../vehicle_api"
  type    = string
}

variable "app_lambda_resolver" {
  default = "api_resolver.entrypoint"
  type    = string
}

variable "app_version" {
  default = "0.1.0-rc"
  type    = string
}

variable "app_name" {
  default = "vehicle-api"
  type    = string
}

variable "env" {
  type = string
}
