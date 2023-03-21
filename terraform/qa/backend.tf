terraform {
  backend "s3" {
    bucket  = "vehicle-api-backend-qa"
    region  = "eu-west-1"
    key     = "qa.tf"
  }
}
