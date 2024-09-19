output "certificate_arn" {
  value = aws_acm_certificate.certificate.arn
}

# ---

variable "zone_name" {
  type = string
}

variable "domain_name" {
  type = string
}

# ---

resource "aws_acm_certificate_validation" "certificate_validation" {
  validation_record_fqdns = [for record in aws_route53_record.record : record.fqdn]
  certificate_arn         = aws_acm_certificate.certificate.arn
}

resource "aws_acm_certificate" "certificate" {
  domain_name       = "${var.domain_name}.${var.zone_name}"
  validation_method = "DNS"
}

data "aws_route53_zone" "public" {
  name = var.zone_name
}

resource "aws_route53_record" "record" {
  for_each = {
    for dvo in aws_acm_certificate.certificate.domain_validation_options : dvo.domain_name => {
      record = dvo.resource_record_value
      name   = dvo.resource_record_name
      type   = dvo.resource_record_type
    }
  }
  allow_overwrite = true
  zone_id         = data.aws_route53_zone.public.zone_id
  records         = [each.value.record]
  name            = each.value.name
  type            = each.value.type
  ttl             = 60
}

# {...}