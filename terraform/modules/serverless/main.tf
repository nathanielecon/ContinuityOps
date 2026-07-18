# ContinuityOps serverless queue worker module (design + IAM placeholders)
# Claim ceiling: L1 — no live Lambda/SQS apply in this repository phase.

variable "enable_serverless" {
  type    = bool
  default = false
}

variable "queue_name" {
  type    = string
  default = "continuityops-worker"
}

locals {
  long_lived_keys = false
}

# Placeholder resources gated by enable_serverless (default false).
# When enabled under OIDC lab apply, create SQS + DLQ + Lambda + IAM role.
# This file documents the composition; terraform apply is not claimed here.

output "serverless_enabled" {
  value = var.enable_serverless
}

output "long_lived_keys" {
  value = local.long_lived_keys
}

output "queue_name" {
  value = var.queue_name
}
