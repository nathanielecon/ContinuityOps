# GitHub OIDC + least-privilege role placeholders (no long-lived keys).

variable "github_repo" {
  type = string
}

variable "environment" {
  type = string
}

variable "aws_account_id" {
  type        = string
  description = "PLACEHOLDER account id"
  default     = "000000000000"
}

variable "enable_iam_resources" {
  type    = bool
  default = false
}

locals {
  role_name = "continuityops-${var.environment}-oidc"
  # Trust subject placeholders — refine when OIDC is wired in hosted workflows.
  oidc_sub_plan  = "repo:${var.github_repo}:environment:${var.environment}-plan"
  oidc_sub_apply = "repo:${var.github_repo}:environment:${var.environment}"
}

output "role_interface" {
  value = {
    role_name        = local.role_name
    plan_subject     = local.oidc_sub_plan
    apply_subject    = local.oidc_sub_apply
    enable_guard     = var.enable_iam_resources
    least_privilege  = true
    long_lived_keys  = false
  }
}
