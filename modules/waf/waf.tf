variable "resource_arns" {
  type = list(string)
}

variable "name" {
  type = string
}

# ---

locals {
  rules = ["AWSManagedRulesCommonRuleSet"] # => Add additional Rules if required
}

# "aws_wafv2_web_acl_logging_configuration" {}
# Todo

resource "aws_wafv2_web_acl_association" "web_acl_associations" {
  count        = length(var.resource_arns)
  web_acl_arn  = aws_wafv2_web_acl.web_acl.arn
  resource_arn = var.resource_arns[count.index]
}

resource "aws_wafv2_web_acl" "web_acl" {
  scope = "REGIONAL"
  name  = var.name

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = var.name
    sampled_requests_enabled   = true
  }

  default_action {
    allow {}
  }

  rule {
    name     = "IpRateLimiter"
    priority = length(local.rules) + 1
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "${var.name}-ip-rate-limiter"
      sampled_requests_enabled   = true
    }
    statement {
      rate_based_statement {
        limit              = 100
        aggregate_key_type = "IP" # Todo: We can also add Rate-Limiter for certain Endpoints!
      }
    }
    action {
      block {}
    }
  }

  dynamic "rule" {
    for_each = { for index, value in local.rules : index => value }
    content {
      name     = rule.value
      priority = rule.key+1

      visibility_config {
        cloudwatch_metrics_enabled = true
        metric_name                = "${var.name}-${rule.value}"
        sampled_requests_enabled   = true
      }
      statement {
        managed_rule_group_statement {
          name        = rule.value
          vendor_name = "AWS"
        }
      }
      override_action {
        none {}
      }
    }
  }
}

# {...}
