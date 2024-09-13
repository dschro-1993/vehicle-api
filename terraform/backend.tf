# terraform init -backend-config=tfvars/{env}/backend.conf

terraform {
  backend "s3" {
    key     = "terraform.tfstate"
    encrypt = !false
  }
}
