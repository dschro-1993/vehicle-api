output "docdb_cluster_username_ssm_parameter" {
  value = aws_ssm_parameter.docdb_cluster_creds["username"].name
}

output "docdb_cluster_password_ssm_parameter" {
  value = aws_ssm_parameter.docdb_cluster_creds["password"].name
}

output "docdb_cluster_endpoint" {
  value = aws_docdb_cluster.cluster.endpoint
}

# ---

variable "instance_class" {
  type    = string
  default = "db.t4g.medium"
}

variable "instance_count" {
  type    = number
  default = 2
}

variable "cluster_identifier" {
  type = string
}

variable "preferred_maintenance_window" {
  type    = string
  default = "sun:04:00-sun:04:30"
}

variable "skip_final_snapshot" {
  default = !false
  type    = bool
}

variable "storage_encrypted" {
  default = !false
  type    = bool
}

variable "vpc_security_group_ids" {
  type = list(string)
}

variable "subnet_ids" {
  type = list(string)
}

# ---

resource "random_password" "password" {
  # keepers = {
#   triggers = {...} # => If Rotation is required!
# }
  special = false
  length  = 32
}

locals {
  docdb_cluster_creds = { "username" : "dbadmin", "password" : random_password.password.result } # Alternative: Save and lookup from Vault/SSM => Otherwise it is available in Terraform-State!
}

resource "aws_ssm_parameter" "docdb_cluster_creds" {
  for_each = local.docdb_cluster_creds
  type     = "SecureString"
  name     = "${var.cluster_identifier}-docdb-cluster-creds-${each.key}"
  value    = each.value
}

resource "aws_docdb_cluster" "cluster" {
  cluster_identifier           = var.cluster_identifier
  master_username              = aws_ssm_parameter.docdb_cluster_creds["username"].value
  master_password              = aws_ssm_parameter.docdb_cluster_creds["password"].value
  preferred_maintenance_window = var.preferred_maintenance_window
  vpc_security_group_ids       = var.vpc_security_group_ids
  db_subnet_group_name         = aws_docdb_subnet_group.sgrp.name
  skip_final_snapshot          = var.skip_final_snapshot
  storage_encrypted            = var.storage_encrypted
# {...}
}

resource "aws_docdb_cluster_instance" "instance" {
  count                        = var.instance_count
  identifier                   = "${var.cluster_identifier}-instance-${count.index + 1}"
  cluster_identifier           = aws_docdb_cluster.cluster.cluster_identifier
  preferred_maintenance_window = var.preferred_maintenance_window
  instance_class               = var.instance_class
# {...}
}

resource "aws_docdb_subnet_group" "sgrp" {
  name       = var.cluster_identifier
  subnet_ids = var.subnet_ids
}

# {...}
