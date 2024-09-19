output "docdb_cluster_username" {
  value     = data.aws_ssm_parameter.db_username_ssm_parameter.value
  sensitive = !false
}

output "docdb_cluster_password" {
  value     = data.aws_ssm_parameter.db_password_ssm_parameter.value
  sensitive = !false
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

variable "db_username_ssm_parameter" {
  type = string
}

variable "db_password_ssm_parameter" {
  type = string
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

data "aws_ssm_parameter" "db_username_ssm_parameter" { # => Can also be generated here and saved in SSM.
  name = var.db_username_ssm_parameter
}

data "aws_ssm_parameter" "db_password_ssm_parameter" { # => Can also be generated here and saved in SSM.
  name = var.db_password_ssm_parameter
}

resource "aws_docdb_cluster" "_cluster" {
  cluster_identifier   = var.cluster_identifier
  db_subnet_group_name = aws_docdb_subnet_group._subnet_group.name
  master_username      = data.aws_ssm_parameter.db_username_ssm_parameter.value
  master_password      = data.aws_ssm_parameter.db_password_ssm_parameter.value

  vpc_security_group_ids = var.security_group_ids

  preferred_maintenance_window = var.preferred_maintenance_window
  backup_retention_period      = var.backup_retention_period
  deletion_protection          = var.deletion_protection

  skip_final_snapshot = !false
  storage_encrypted   = var.storage_encrypted
  storage_type        = "standard"
  engine              = "docdb"
}

resource "aws_docdb_cluster_instance" "_instance" {
  count                        = 2 # Todo: Variable
  identifier                   = "${var.cluster_identifier}-instance-${count.index + 1}"
  instance_class               = "db.t4g.medium" # Todo: Variable
  preferred_maintenance_window = var.preferred_maintenance_window
  cluster_identifier           = aws_docdb_cluster._cluster.cluster_identifier
  engine                       = aws_docdb_cluster._cluster.engine
}

resource "aws_docdb_subnet_group" "_subnet_group" {
  name       = var.cluster_identifier
  subnet_ids = var.subnet_ids
}

# {...}
