# ContinuityOps serverless queue worker — live when enable_serverless=true.

variable "enable_serverless" {
  type    = bool
  default = false
}

variable "environment" {
  type    = string
  default = "staging"
}

variable "queue_name" {
  type    = string
  default = "continuityops-worker"
}

variable "lambda_role_arn" {
  type    = string
  default = ""
}

locals {
  long_lived_keys = false
  fn_name         = "${var.queue_name}-${var.environment}"
}

resource "aws_sqs_queue" "dlq" {
  count                     = var.enable_serverless ? 1 : 0
  name                      = "${var.queue_name}-${var.environment}-dlq"
  message_retention_seconds = 1209600

  tags = {
    Project     = "continuityops"
    Environment = var.environment
    Purpose     = "dlq"
  }
}

resource "aws_sqs_queue" "worker" {
  count                      = var.enable_serverless ? 1 : 0
  name                       = "${var.queue_name}-${var.environment}"
  visibility_timeout_seconds = 60
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dlq[0].arn
    maxReceiveCount     = 3
  })

  tags = {
    Project     = "continuityops"
    Environment = var.environment
    Purpose     = "worker-queue"
  }
}

data "archive_file" "lambda_zip" {
  count       = var.enable_serverless ? 1 : 0
  type        = "zip"
  output_path = "${path.module}/.build/worker.zip"
  source {
    content  = <<-EOF
      exports.handler = async (event) => {
        console.log(JSON.stringify({ ok: true, records: (event.Records || []).length }));
        return { ok: true };
      };
    EOF
    filename = "index.js"
  }
}

resource "aws_lambda_function" "worker" {
  count            = var.enable_serverless ? 1 : 0
  function_name    = local.fn_name
  role             = var.lambda_role_arn
  handler          = "index.handler"
  runtime          = "nodejs20.x"
  filename         = data.archive_file.lambda_zip[0].output_path
  source_code_hash = data.archive_file.lambda_zip[0].output_base64sha256
  timeout          = 30

  environment {
    variables = {
      QUEUE_URL   = aws_sqs_queue.worker[0].url
      ENVIRONMENT = var.environment
      PROJECT     = "continuityops"
    }
  }

  tags = {
    Project     = "continuityops"
    Environment = var.environment
  }

  depends_on = [aws_sqs_queue.worker]
}

resource "aws_lambda_event_source_mapping" "sqs" {
  count            = var.enable_serverless ? 1 : 0
  event_source_arn = aws_sqs_queue.worker[0].arn
  function_name    = aws_lambda_function.worker[0].arn
  batch_size       = 5
  enabled          = true
}

output "serverless_enabled" {
  value = var.enable_serverless
}

output "long_lived_keys" {
  value = local.long_lived_keys
}

output "queue_name" {
  value = var.queue_name
}

output "queue_url" {
  value = try(aws_sqs_queue.worker[0].url, null)
}

output "lambda_function_name" {
  value = try(aws_lambda_function.worker[0].function_name, null)
}
