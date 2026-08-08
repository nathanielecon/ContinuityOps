# Grant continuityops-gha the permissions it needs to manage this root.
#
# WHY THIS IS SAFE DESPITE THE ROLE NOT BEING TERRAFORM-MANAGED:
# `aws_iam_role_policy_attachment` references the role by NAME. Terraform attaches
# a policy without importing or owning the role, so its OIDC trust policy is never
# read, planned, or modified. That was the whole risk in splitting the role
# (BF-2026-030) — a wrong trust condition locks CI out of the account. Attaching a
# policy carries none of it.
#
# ON SELF-GRANTING: this lets the deploy role widen its own permissions, which is
# normally a red flag. Worth being precise about what changes: the role already
# holds IAM write (it created the users, roles, policies and attachments in this
# root), so it could already grant itself anything. This makes an existing
# capability explicit and reviewable in git rather than adding a new one. The
# alternative — a human pasting JSON into the console — leaves no audit trail and
# drifts from the repo.

variable "attach_gha_finops_addon" {
  type        = bool
  default     = true
  description = <<-EOT
    Attach the FinOps addon policy to the deploy role. Set false if the role lacks
    iam:AttachRolePolicy on itself, in which case attach
    terraform/policies/continuityops-gha-finops-addon.json by hand and re-apply.
  EOT
}

locals {
  # Single source of truth is the JSON file, so the documented policy and the
  # applied policy cannot drift. The file carries `_comment` / `_scope_note` keys
  # for human readers; IAM rejects unknown top-level keys, so only Version and
  # Statement are forwarded.
  gha_addon_raw = jsondecode(
    file("${path.module}/../../policies/continuityops-gha-finops-addon.json")
  )

  gha_addon_policy = {
    Version   = local.gha_addon_raw.Version
    Statement = local.gha_addon_raw.Statement
  }
}

resource "aws_iam_policy" "gha_finops_addon" {
  count       = var.attach_gha_finops_addon ? 1 : 0
  name        = "ContinuityOpsGhaFinOpsAddon"
  description = "Budgets + Cost Anomaly Detection management for the deploy role. Create-only; grants no data access."

  policy = jsonencode(local.gha_addon_policy)
}

resource "aws_iam_role_policy_attachment" "gha_finops_addon" {
  count      = var.attach_gha_finops_addon ? 1 : 0
  role       = var.gha_role_name
  policy_arn = aws_iam_policy.gha_finops_addon[0].arn
}

output "gha_finops_addon" {
  value = var.attach_gha_finops_addon ? {
    policy_arn                   = aws_iam_policy.gha_finops_addon[0].arn
    attached_to                  = var.gha_role_name
    role_imported_into_terraform = false
    trust_policy_touched         = false
  } : null
}
