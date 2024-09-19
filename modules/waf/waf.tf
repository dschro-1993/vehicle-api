variable "wacl_resource_arn" {
  type = string
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

resource "aws_wafv2_web_acl_association" "web_acl_association" {
  web_acl_arn  = aws_wafv2_web_acl.web_acl.arn
  resource_arn = var.wacl_resource_arn
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
    name     = "QuotaRule"
    priority = length(local.rules) + 1
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "${var.name}-quota-rule"
      sampled_requests_enabled   = true
    }
    statement {
      rate_based_statement {
        limit              = 100
        aggregate_key_type = "IP"
      }
    }
    action {
      block {}
    }
  }

  dynamic "rule" {
    for_each = { for x in local.rules : x => x }
    content {
      name     = rule.key
      priority = index(local.rules, rule.key) + 1

      visibility_config {
        cloudwatch_metrics_enabled = true
        metric_name                = "${var.name}-${rule.key}"
        sampled_requests_enabled   = true
      }
      statement {
        managed_rule_group_statement {
          name        = rule.key
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
