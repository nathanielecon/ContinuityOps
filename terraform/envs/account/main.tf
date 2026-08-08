# Account-level cost guardrails (BF-2026-029).
#
# This root is deliberately SEPARATE from envs/staging and is NEVER destroyed:
# a budget guard that gets torn down with the lab it polices is not a guard.
# `teardown.yml` does not offer `account` as an option.
#
# Everything here is free: AWS Budgets gives two action-enabled budgets at no
# charge, and Cost Anomaly Detection is free.

variable "alert_email" {
  type        = string
  description = <<-EOT
    Destination for budget and anomaly alerts. Intentionally has NO default —
    this repository is public, so the address must not be committed. Supply it at
    apply time via TF_VAR_alert_email, sourced from repository variable
    COPS_ALERT_EMAIL. A missing value fails the apply, which is correct: a
    guardrail nobody is notified about is not a guardrail.
  EOT

  validation {
    condition     = can(regex("^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$", var.alert_email))
    error_message = "alert_email must be a valid email address."
  }
}

variable "gha_role_name" {
  type        = string
  description = "Deploy role frozen when the budget action fires."
  default     = "continuityops-gha"
}

locals {
  # operations/finops/budgets.json was previously documentation with
  # "claim_ceiling": "L1" and no deployed effect. Reading it here makes it the
  # actual source of truth: edit the JSON, re-apply, the real budget changes.
  finops = jsondecode(file("${path.module}/../../../operations/finops/budgets.json"))

  budget_limit_usd = tostring(local.finops.monthly_budget_usd)
}

# ---------------------------------------------------------------------------
# Monthly cost budget + notifications
# ---------------------------------------------------------------------------

resource "aws_budgets_budget" "monthly" {
  # The deploy role has no budgets:ModifyBudget until the addon is attached
  # (runs 31267523721 and 31271867281 both failed here). Terraform cannot infer
  # that ordering, so state it.
  depends_on = [aws_iam_role_policy_attachment.gha_finops_addon]

  name         = "continuityops-monthly"
  budget_type  = "COST"
  limit_amount = local.budget_limit_usd
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  # Thresholds mirror operations/finops/budgets.json.
  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 50
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.alert_email]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.alert_email]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.alert_email]
  }

  # Forecast alert is the one that would have caught BF-2026-029 early: a
  # $14.40/day run rate forecasts past any sane monthly cap within days, long
  # before actual spend crosses it.
  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = [var.alert_email]
  }
}

# ---------------------------------------------------------------------------
# Budget action: freeze provisioning at 100% of budget
# ---------------------------------------------------------------------------

# CRITICAL DESIGN POINT: this policy denies resource CREATION only. It must
# never deny Delete*/Terminate* actions. If breaching the budget also removed
# the ability to tear down, the guardrail would trap you in the expensive state
# it exists to escape — strictly worse than no guardrail at all.
resource "aws_iam_policy" "deny_provisioning" {
  name        = "continuityops-budget-deny-provisioning"
  description = "Attached to the deploy role by a budget action at 100%. Denies creates, never deletes."

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "DenyExpensiveProvisioning"
        Effect = "Deny"
        Action = [
          "eks:CreateCluster",
          "eks:CreateNodegroup",
          "eks:CreateFargateProfile",
          "ec2:RunInstances",
          "ec2:CreateNatGateway",
          "ec2:AllocateAddress",
          "elasticloadbalancing:CreateLoadBalancer",
          "rds:CreateDBInstance",
          "rds:CreateDBCluster",
          "ecs:CreateCluster",
          "ecs:CreateService",
          "elasticache:CreateCacheCluster",
        ]
        Resource = "*"
      },
    ]
  })
}

data "aws_iam_policy_document" "budget_action_assume" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["budgets.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "budget_action" {
  name               = "continuityops-budget-action"
  description        = "Assumed by AWS Budgets to attach the deny-provisioning policy."
  assume_role_policy = data.aws_iam_policy_document.budget_action_assume.json
}

resource "aws_iam_role_policy_attachment" "budget_action" {
  role       = aws_iam_role.budget_action.name
  policy_arn = "arn:aws:iam::aws:policy/AWSBudgetsActionsWithAWSResourceControlAccess"
}

resource "aws_budgets_budget_action" "freeze_provisioning" {
  budget_name        = aws_budgets_budget.monthly.name
  action_type        = "APPLY_IAM_POLICY"
  approval_model     = "AUTOMATIC"
  notification_type  = "ACTUAL"
  execution_role_arn = aws_iam_role.budget_action.arn

  action_threshold {
    action_threshold_type  = "PERCENTAGE"
    action_threshold_value = 100
  }

  definition {
    iam_action_definition {
      policy_arn = aws_iam_policy.deny_provisioning.arn
      roles      = [var.gha_role_name]
    }
  }

  subscriber {
    address           = var.alert_email
    subscription_type = "EMAIL"
  }
}

# ---------------------------------------------------------------------------
# Cost Anomaly Detection
# ---------------------------------------------------------------------------

# Free. Detects the exact shape of BF-2026-029: a step change from ~$0/day to
# $14.40/day on a single service. The leak ran 21 days because nothing watched.
#
# IMPORTANT (run 31272457415): AWS permits exactly ONE dimensional (SERVICE)
# anomaly monitor per account, and this account already has one — the create
# failed with `ValidationException: Limit exceeded on dimensional spend monitor
# creation`, NOT AccessDenied. So service-level anomaly *detection* is already
# active account-wide; what is missing is a *subscription* routing its findings
# to an inbox.
#
# Therefore this resource defaults to OFF. Creating it can never succeed while
# another dimensional monitor exists, and a permanently-failing resource blocks
# every apply of this root — including the budget, which is the guardrail that
# actually enforces anything.
variable "create_anomaly_monitor" {
  type        = bool
  default     = false
  description = "Create a dimensional monitor. Only possible if the account has none; AWS allows one."
}

variable "existing_anomaly_monitor_arn" {
  type        = string
  default     = ""
  description = <<-EOT
    ARN of the account's existing dimensional monitor. When set, the alert
    subscription attaches to it instead of creating a new monitor. Find it with:
      aws ce get-anomaly-monitors --query 'AnomalyMonitors[].[MonitorArn,MonitorDimension]'
    (ce:GetAnomalyMonitors is granted by the FinOps addon.)
  EOT
}

locals {
  anomaly_monitor_arn = var.create_anomaly_monitor ? one(aws_ce_anomaly_monitor.service[*].arn) : var.existing_anomaly_monitor_arn

  # Subscribe only when we have a monitor to subscribe to.
  create_anomaly_subscription = local.anomaly_monitor_arn != ""
}

resource "aws_ce_anomaly_monitor" "service" {
  count = var.create_anomaly_monitor ? 1 : 0

  # Needs ce:CreateAnomalyMonitor from the addon; same ordering reason as the
  # budget above.
  depends_on = [aws_iam_role_policy_attachment.gha_finops_addon]

  name              = "continuityops-service-monitor"
  monitor_type      = "DIMENSIONAL"
  monitor_dimension = "SERVICE"
}

resource "aws_ce_anomaly_subscription" "alerts" {
  count = local.create_anomaly_subscription ? 1 : 0

  name      = "continuityops-anomaly-alerts"
  frequency = "DAILY"

  monitor_arn_list = [local.anomaly_monitor_arn]

  subscriber {
    type    = "EMAIL"
    address = var.alert_email
  }

  # $10 absolute impact — comfortably below one day of an idle EKS control
  # plane on extended support ($14.40), so this fires on day one.
  threshold_expression {
    dimension {
      key           = "ANOMALY_TOTAL_IMPACT_ABSOLUTE"
      match_options = ["GREATER_THAN_OR_EQUAL"]
      values        = ["10"]
    }
  }
}

# ---------------------------------------------------------------------------
# Outputs
# ---------------------------------------------------------------------------

output "budget_name" {
  value = aws_budgets_budget.monthly.name
}

output "budget_limit_usd" {
  value       = local.budget_limit_usd
  description = "Sourced from operations/finops/budgets.json."
}

output "guardrails" {
  value = {
    budget_notifications  = ["50%", "80%", "100%", "100% forecasted"]
    freeze_action_at      = "100% actual"
    freeze_denies_deletes = false
    destroyed_by_teardown = false

    anomaly_monitor_created = var.create_anomaly_monitor
    anomaly_subscription    = local.create_anomaly_subscription ? "DAILY, >= $10 absolute impact" : "NOT WIRED — set existing_anomaly_monitor_arn"
    anomaly_detection_note  = "The account already has a dimensional SERVICE monitor, so detection is active; only alert routing needs the subscription."
  }
}
