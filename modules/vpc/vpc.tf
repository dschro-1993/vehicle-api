output "tier1_security_group_ids" {
  value = [aws_security_group.tier1_security_group.id]
}

output "tier2_security_group_ids" {
  value = [aws_security_group.tier2_security_group.id]
}

output "tier3_security_group_ids" {
  value = [aws_security_group.tier3_security_group.id]
}

output "tier1_subnets_ids" {
  value = aws_subnet.tier1_subnets[*].id
}

output "tier2_subnets_ids" {
  value = aws_subnet.tier2_subnets[*].id
}

output "tier3_subnets_ids" {
  value = aws_subnet.tier3_subnets[*].id
}

output "vpc_id" {
  value = aws_vpc.this.id
}

# ---

variable "name" {
  type    = string
  default = "my-custom-vpc"
}

variable "cidr_block" {
  type    = string
  default = "10.0.0.0/16"
}

variable "tier1_subnets" {
  type    = list(string)
  default = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]
}

variable "tier2_subnets" {
  type    = list(string)
  default = ["10.0.21.0/24", "10.0.22.0/24", "10.0.23.0/24"]
}

variable "tier3_subnets" {
  type    = list(string)
  default = ["10.0.31.0/24", "10.0.32.0/24", "10.0.33.0/24"]
}

variable "azs" {
  type = list(string)
  default = [
    "eu-west-1a",
    "eu-west-1b",
    "eu-west-1c",
  ]
}

# ---

resource "aws_vpc" "this" {
  cidr_block           = var.cidr_block
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = var.name
  # {...}
  }
}

resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id
}

resource "aws_subnet" "tier1_subnets" {
  count             = length(var.tier1_subnets)
  vpc_id            = aws_vpc.this.id
  cidr_block        = var.tier1_subnets[count.index]
  availability_zone = var.azs[count.index]
}

resource "aws_subnet" "tier2_subnets" {
  count             = length(var.tier2_subnets)
  vpc_id            = aws_vpc.this.id
  cidr_block        = var.tier2_subnets[count.index]
  availability_zone = var.azs[count.index]
}

resource "aws_subnet" "tier3_subnets" {
  count             = length(var.tier3_subnets)
  vpc_id            = aws_vpc.this.id
  cidr_block        = var.tier3_subnets[count.index]
  availability_zone = var.azs[count.index]
}

resource "aws_eip" "eips" {
  count  = length(var.tier1_subnets)
  domain = "vpc"
}

resource "aws_nat_gateway" "ngws" {
  count         = length(var.tier1_subnets)
  allocation_id = aws_eip.eips[count.index].id
  subnet_id     = aws_subnet.tier1_subnets[count.index].id
}

resource "aws_route_table" "tier1" {
  vpc_id = aws_vpc.this.id
}

resource "aws_route_table" "tier2_tables" {
  count  = length(var.tier2_subnets)
  vpc_id = aws_vpc.this.id
}

resource "aws_route_table" "tier3" {
  vpc_id = aws_vpc.this.id
}

resource "aws_route_table_association" "tier1" {
  count          = length(aws_subnet.tier1_subnets)
  subnet_id      = aws_subnet.tier1_subnets[count.index].id
  route_table_id = aws_route_table.tier1.id
}

resource "aws_route_table_association" "tier2" {
  count          = length(aws_subnet.tier2_subnets)
  subnet_id      = aws_subnet.tier2_subnets[count.index].id
  route_table_id = aws_route_table.tier2_tables[count.index].id
}

resource "aws_route_table_association" "tier3" {
  count          = length(aws_subnet.tier3_subnets)
  subnet_id      = aws_subnet.tier3_subnets[count.index].id
  route_table_id = aws_route_table.tier3.id
}

resource "aws_route" "tier1_access" {
  route_table_id         = aws_route_table.tier1.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.this.id
}

resource "aws_route" "tier2_access" {
  count = length(aws_subnet.tier2_subnets)

  route_table_id         = aws_route_table.tier2_tables[count.index].id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.ngws[count.index].id
}

resource "aws_security_group" "tier1_security_group" {
  name   = "tier1"
  vpc_id = aws_vpc.this.id
  ingress {
    cidr_blocks = ["0.0.0.0/0"]
    protocol    = "tcp"
    from_port   = 443
    to_port     = 443
  }
  egress {
    cidr_blocks = ["0.0.0.0/0"]
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
  }
}

resource "aws_security_group" "tier2_security_group" {
  name   = "tier2"
  vpc_id = aws_vpc.this.id
  egress {
    cidr_blocks = ["0.0.0.0/0"]
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
  }
}

resource "aws_security_group" "tier3_security_group" {
  name   = "tier3"
  vpc_id = aws_vpc.this.id
  ingress {
    security_groups = [aws_security_group.tier2_security_group.id]
    protocol        = "tcp"
    from_port       = 27017
    to_port         = 27017
  }
}

data "aws_vpc_endpoint_service" "ssm" { # => Respects Provider-Region and simplifies lookup!
  service = "ssm"
}

resource "aws_vpc_endpoint" "ssm" {
  vpc_id              = aws_vpc.this.id
  private_dns_enabled = !false
  service_name        = data.aws_vpc_endpoint_service.ssm.service_name
  vpc_endpoint_type   = "Interface"
  security_group_ids  = [aws_security_group.tier2_ssm_vpce.id]
  subnet_ids          = aws_subnet.tier2_subnets[*].id
}

resource "aws_security_group" "tier2_ssm_vpce" {
  name   = "ssm-vpce"
  vpc_id = aws_vpc.this.id
  ingress {
    cidr_blocks = ["0.0.0.0/0"]
    protocol    = "tcp"
    from_port   = 443
    to_port     = 443
  }
}

# TODO

# resource "aws_network_acl_association" "this" {
#   for_each       = { for x in concat(aws_subnet.tier1_subnets[*], aws_subnet.tier2_subnets[*], aws_subnet.tier3_subnets[*]) : x.id => x }
#   network_acl_id = aws_network_acl.this.id
#   subnet_id      = each.key
# }

# resource "aws_network_acl" "this" {
#   vpc_id = aws_vpc.this.id
#   ingress {
#     action     = "allow"
#     cidr_block = "0.0.0.0/0"
#     protocol   = "-1"
#     rule_no    = 100
#     from_port  = 0
#     to_port    = 0
#   }
#   egress {
#     action     = "allow"
#     cidr_block = "0.0.0.0/0"
#     protocol   = "-1"
#     rule_no    = 100
#     from_port  = 0
#     to_port    = 0
#   }
# }

# {...}
