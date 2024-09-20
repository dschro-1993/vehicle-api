output "docdb_cluster_username_ssm_parameter" {
  value = aws_ssm_parameter.docdb_cluster_creds["username"].name
}

output "docdb_cluster_password_ssm_parameter" {
  value = aws_ssm_parameter.docdb_cluster_creds["password"].name
}

output "docdb_cluster_endpoint" {
  value = aws_docdb_cluster._cluster.endpoint
}

# ---

variable "preferred_maintenance_window" {
  default = "sun:04:00-sun:04:30"
  type    = string
}

variable "backup_retention_period" {
  default = 7
  type    = number
}

variable "deletion_protection" {
  default = false # Should be "True" in prod!
  type    = bool
}

variable "storage_encrypted" {
  default = !false
  type    = bool
}

variable "cluster_identifier" {
  type = string
}

variable "security_group_ids" {
  type = list(string)
}

variable "subnet_ids" {
  type = list(string)
}

# ---

resource "random_password" "password" {
  length  = 32
  special = false
# keepers = {
#   triggers = {...} # => If Rotation is required!
# }
}

locals {
  docdb_cluster_creds = { "username" : "dbadmin", "password" : random_password.password.result } # Todo: Save and lookup from Vault/SSM => Otherwise it is available in Terraform-State!
}

resource "aws_ssm_parameter" "docdb_cluster_creds" {
  for_each = local.docdb_cluster_creds
  type     = "SecureString"
  name     = "${var.cluster_identifier}-docdb-cluster-creds-${each.key}"
  value    = each.value
}

resource "aws_docdb_cluster" "_cluster" {
  cluster_identifier           = "${var.cluster_identifier}-db"
  master_username              = aws_ssm_parameter.docdb_cluster_creds["username"].value
  master_password              = aws_ssm_parameter.docdb_cluster_creds["password"].value
  skip_final_snapshot          = !false
  db_subnet_group_name         = aws_docdb_subnet_group._db_subnet_group.name
  vpc_security_group_ids       = var.security_group_ids
  preferred_maintenance_window = var.preferred_maintenance_window
  backup_retention_period      = var.backup_retention_period
  deletion_protection          = var.deletion_protection
  storage_encrypted            = var.storage_encrypted
  storage_type                 = "standard"
  engine                       = "docdb"
}

resource "aws_docdb_cluster_instance" "_instance" {
  count                        = 2 # Todo: Variable
  identifier                   = "${var.cluster_identifier}-instance-${count.index + 1}"
  instance_class               = "db.t4g.medium" # Todo: Variable
  preferred_maintenance_window = var.preferred_maintenance_window
  cluster_identifier           = aws_docdb_cluster._cluster.cluster_identifier
  engine                       = aws_docdb_cluster._cluster.engine
}

resource "aws_docdb_subnet_group" "_db_subnet_group" {
  name       = var.cluster_identifier
  subnet_ids = var.subnet_ids
}

# {...}
