variable "security_group_ids" {
  type = list(string)
}

variable "subnet_ids" {
  type = list(string)
}

variable "root_dir" {
  type = string
}

variable "code_dir" {
  type = string
}

variable "target_group_arn" {
  type = string
}

variable "lambda_layer_output_file" {
  type = string
}

variable "lambda_layer_output_path" {
  type = string
}

variable "lambda_handler" {
  type = string
}

variable "lambda_name" {
  type = string
}

variable "env_vars" {
  type = map(any)
}

# ---

resource "null_resource" "custom_requirements" {
  # triggers = {
  #   pyproject = filesha256("${var.root_dir}/pyproject.toml")
  # }
  provisioner "local-exec" {
    command = <<EOT
      rm -rf ${var.root_dir}/.venv
      rm -rf ${var.lambda_layer_output_path}
      poetry install --no-dev -C ${var.root_dir}
      mkdir  ${var.lambda_layer_output_path}
      cp -rf ${var.root_dir}/.venv/lib ${var.lambda_layer_output_path}
      zip -r ${var.lambda_layer_output_file} ${var.lambda_layer_output_path}
      rm -rf ${var.lambda_layer_output_path}
    EOT
  }
}

resource "aws_s3_bucket" "layer_bucket" {
  bucket = "${var.lambda_name}-layer-bucket"
}

# {lifecycle-rules}
# {...}

resource "aws_s3_object" "layer_object" {
  depends_on  = [null_resource.custom_requirements]
  bucket      = aws_s3_bucket.layer_bucket.id
# source_hash = filesha256("${var.lambda_layer_output_file}")
  source      = var.lambda_layer_output_file
  key         = var.lambda_layer_output_file
}

resource "aws_lambda_layer_version" "custom_layer" {
  layer_name               = "${var.lambda_name}-custom-layer"
  compatible_architectures = ["arm64"]
  compatible_runtimes      = ["python3.12"]
  s3_bucket                = aws_s3_bucket.layer_bucket.id
  s3_key                   = aws_s3_object.layer_object.id
}

# {...}

resource "aws_iam_role" "iam_role" {
  name = "${var.lambda_name}-role"
  path = "/service-role/"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Principal = { Service = "lambda.amazonaws.com" }
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
      }
    ]
  })
}

resource "aws_iam_role_policy" "iam_role_policy" {
  name = "custom"
  role = aws_iam_role.iam_role.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Resource = "*" # Todo
        Action   = ["ssm:GetParameters", "ssm:GetParameter", "kms:Decrypt"]
        Effect   = "Allow"
      },
      {
        Resource = "*" # Todo
        Action   = ["xray:PutTraceSegments"]
        Effect   = "Allow"
      },
    ]
  })
}

# resource "aws_iam_role_policy_attachment" "cwl_attachment" {
# role       = aws_iam_role.iam_role.name
# policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
# }

# Includes CWL-Permissions already!
resource "aws_iam_role_policy_attachment" "vpc_attachment" {
  role       = aws_iam_role.iam_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

data "archive_file" "archive" {
  type        = "zip"
  output_path = "archive.zip"
  source_dir  = var.code_dir
}

resource "aws_lambda_permission" "lambda_permission" {
  source_arn    = var.target_group_arn
  function_name = aws_lambda_function.lambda.function_name
  principal     = "elasticloadbalancing.amazonaws.com" # Todo: Variable
  action        = "lambda:InvokeFunction"
}

resource "aws_lb_target_group_attachment" "target_group_attachment" {
  depends_on       = [aws_lambda_permission.lambda_permission]
  target_group_arn = var.target_group_arn
  target_id        = aws_lambda_function.lambda.arn
}

data "aws_region" "current" {}

resource "aws_lambda_function" "lambda" {
  function_name = "${var.lambda_name}-handler"

  handler = var.lambda_handler
  runtime = "python3.12"
  timeout = 10

  filename         = data.archive_file.archive.output_path
  source_code_hash = data.archive_file.archive.output_base64sha256

  layers = [
    "arn:aws:lambda:${data.aws_region.current.name}:017000801446:layer:AWSLambdaPowertoolsPythonV2-Arm64:79",
    aws_lambda_layer_version.custom_layer.arn
  ]

  vpc_config {
    security_group_ids = var.security_group_ids
    subnet_ids         = var.subnet_ids
  }

  role          = aws_iam_role.iam_role.arn
  architectures = ["arm64"] # Use Graviton2

  environment {
    variables = var.env_vars
  }

  tracing_config {
    mode = "Active"
  }
}

# {...}
