output "target_group_arn" {
  value = aws_lb_target_group.target_group.arn
}

output "alb_arn" {
  value = aws_lb.lb.arn
}

# ---

variable "name" {
  type = string
}

variable "zone_name" {
  type = string
}

variable "domain_name" {
  type = string
}

variable "target_type" {
  type = string
}

variable "certificate_arn" {
  type = string
}

variable "healthcheck_path" {
  default = "/"
  type    = string
}

variable "healthcheck_port" {
  default = "traffic-port"
  type    = string
}

variable "vpc_security_group_ids" {
  type = list(string)
}

variable "subnet_ids" {
  type = list(string)
}

variable "vpc_id" {
  type = string
}

# ---

data "aws_route53_zone" "r53_zone" {
  name = var.zone_name
}

resource "aws_route53_record" "alias_record" {
  alias {
    name    = aws_lb.lb.dns_name
    zone_id = aws_lb.lb. zone_id
    evaluate_target_health = false
  }
  name    = "${var.domain_name}.${var.zone_name}"
  zone_id = data.aws_route53_zone.r53_zone.zone_id
  type    = "A"
}

resource "aws_lb_target_group" "target_group" {
  name        = var.name
  target_type = var.target_type
  vpc_id      = var.vpc_id

  lambda_multi_value_headers_enabled = !false

  health_check {
    enabled = false # Todo: λs should expose a "/health-check" Endpoint if "True"
    timeout = 10    # Todo: {Value} < `interval` required => Otherwise Exception is Thrown!
    path    = var.target_type == "lambda" ? null : var.healthcheck_path
    port    = var.target_type == "lambda" ? null : var.healthcheck_port
  }
}

resource "aws_lb_listener" "listener" {
  load_balancer_arn = aws_lb.lb.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = var.certificate_arn

  default_action {
    target_group_arn = aws_lb_target_group.target_group.arn
    type             = "forward"
  }
}

resource "aws_lb" "lb" {
  name            = var.name
  security_groups = var.vpc_security_group_ids
  subnets         = var.subnet_ids

  # connection_logs {}
  # access_logs {}

  # {...}
}

# {...}
