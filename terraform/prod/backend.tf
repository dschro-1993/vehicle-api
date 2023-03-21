terraform {
  backend "s3" {
    bucket  = "vehicle-api-backend-prod"
    region  = "eu-west-1"
    key     = "prod.tf"
  }
}
