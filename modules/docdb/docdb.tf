output "docdb_cluster_username_ssm_parameter" {
  value = aws_ssm_parameter.docdb_cluster_creds[0].name
}

output "docdb_cluster_password_ssm_parameter" {
  value = aws_ssm_parameter.docdb_cluster_creds[1].name
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

locals {
  creds = ["username", "password"]
}

resource "random_string" "docdb_cluster_creds" {
  count  = length(local.creds)
  length = 16
}

resource "aws_ssm_parameter" "docdb_cluster_creds" {
  count = length(local.creds)
  name  = "${var.cluster_identifier}-docdb-cluster-${local.creds[count.index]}"
  value = random_string.docdb_cluster_creds[count.index].id
  type  = "SecureString"
}

resource "aws_docdb_cluster" "_cluster" {
  cluster_identifier           = var.cluster_identifier
  master_username              = random_string.docdb_cluster_creds[0].id
  master_password              = random_string.docdb_cluster_creds[1].id
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
