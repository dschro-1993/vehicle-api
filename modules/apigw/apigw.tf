output "execution_arn" {
  value = "${aws_api_gateway_rest_api.rest_api.execution_arn}/*/*/*"
}

output "stage_arn" {
  value = aws_api_gateway_stage.stage.arn
}

# ---

variable "xray_tracing_enabled" {
  default = !false
  type    = bool
}

variable "zone_name" {
  type = string
}

variable "domain_name" {
  type = string
}

variable "certificate_arn" {
  type = string
}

variable "qualified_invoke_arn" {
  type = string
}

variable "name" {
  type = string
}

# ---

resource "aws_api_gateway_rest_api" "rest_api" {
  name = var.name
  endpoint_configuration { types = ["REGIONAL"] } # Todo: Variable
}

resource "aws_api_gateway_resource" "my_proxy" {
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
  parent_id   = aws_api_gateway_rest_api.rest_api.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "any" {
  authorization = "NONE" # Todo: Add your Cognito-Authorizers here

  rest_api_id = aws_api_gateway_rest_api.rest_api.id
  resource_id = aws_api_gateway_resource.my_proxy.id

  http_method = "ANY"
}

resource "aws_api_gateway_integration" "any" {
  http_method = "ANY"

  depends_on  = [aws_api_gateway_method.any]
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
  resource_id = aws_api_gateway_resource.my_proxy.id

  integration_http_method = "POST" # "POST" is required if Type is: "AWS_PROXY"
  type                    = "AWS_PROXY"
  uri                     = var.qualified_invoke_arn
}

# ---

resource "aws_api_gateway_deployment" "deployment" {
  depends_on  = [ aws_api_gateway_method.any, aws_api_gateway_integration.any ]
  triggers    = { redeployment = sha256(jsonencode(aws_api_gateway_rest_api.rest_api.body)) }
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
  lifecycle { create_before_destroy = true }
}

resource "aws_api_gateway_stage" "stage" {
  deployment_id        = aws_api_gateway_deployment.deployment.id
  rest_api_id          = aws_api_gateway_rest_api.rest_api.id
  xray_tracing_enabled = var.xray_tracing_enabled
  stage_name           = "api"
}

# ---

resource "aws_api_gateway_domain_name" "domain_name" {
  domain_name              = "${var.domain_name}.${var.zone_name}"
  regional_certificate_arn = var.certificate_arn
  endpoint_configuration { types = ["REGIONAL"] } # Todo: Variable
}

resource "aws_route53_record" "alias_record" {
  alias {
    evaluate_target_health = false
    name                   = aws_api_gateway_domain_name.domain_name.regional_domain_name
    zone_id                = aws_api_gateway_domain_name.domain_name.regional_zone_id
  }
  name    = aws_api_gateway_domain_name.domain_name.domain_name
  zone_id = data.aws_route53_zone.r53_zone.zone_id
  type    = "A"
}

resource "aws_api_gateway_base_path_mapping" "mapping" {
  domain_name = aws_api_gateway_domain_name.domain_name.domain_name
  stage_name  = aws_api_gateway_stage.stage.stage_name

  api_id = aws_api_gateway_rest_api.rest_api.id
}

data "aws_route53_zone" "r53_zone" {
  name = var.zone_name
}

# {...}
