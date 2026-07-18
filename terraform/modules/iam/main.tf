# Lab IAM roles (no long-lived access keys).

variable "github_repo" {
  type = string
}

variable "environment" {
  type = string
}

variable "aws_account_id" {
  type        = string
  description = "AWS account id"
  default     = "000000000000"
}

variable "enable_iam_resources" {
  type    = bool
  default = false
}

locals {
  role_name      = "continuityops-${var.environment}-oidc"
  lambda_role    = "continuityops-${var.environment}-lambda"
  oidc_sub_plan  = "repo:${var.github_repo}:environment:${var.environment}-plan"
  oidc_sub_apply = "repo:${var.github_repo}:environment:${var.environment}"
}

data "aws_iam_policy_document" "lambda_assume" {
  count = var.enable_iam_resources ? 1 : 0
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda" {
  count              = var.enable_iam_resources ? 1 : 0
  name               = local.lambda_role
  assume_role_policy = data.aws_iam_policy_document.lambda_assume[0].json

  tags = {
    Project     = "continuityops"
    Environment = var.environment
    ManagedBy   = "terraform"
    Purpose     = "lambda-execution"
  }
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  count      = var.enable_iam_resources ? 1 : 0
  role       = aws_iam_role.lambda[0].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_sqs" {
  count      = var.enable_iam_resources ? 1 : 0
  role       = aws_iam_role.lambda[0].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole"
}

output "role_interface" {
  value = {
    role_name          = local.role_name
    plan_subject       = local.oidc_sub_plan
    apply_subject      = local.oidc_sub_apply
    enable_guard       = var.enable_iam_resources
    least_privilege    = true
    long_lived_keys    = false
    lambda_role_name   = try(aws_iam_role.lambda[0].name, null)
    lambda_role_arn    = try(aws_iam_role.lambda[0].arn, null)
  }
}
