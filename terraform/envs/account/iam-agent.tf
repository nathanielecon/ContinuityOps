# Scoped read-only identity for agent-driven cost/inventory investigation.
#
# Replaces the use of ROOT access keys by the AWS MCP connector (found during
# BF-2026-029: `sts get-caller-identity` returned arn:aws:iam::000000000000:root).
# Root keys can delete the account; AWS guidance is never to create them.
#
# NO ACCESS KEY IS CREATED HERE, deliberately. `aws_iam_access_key` would place
# the secret in Terraform state — which lives in S3 and is readable by anyone who
# can read the bucket — and echo it through plan/apply logs. Mint the key in the
# console instead (IAM > Users > continuityops-agent-ro > Security credentials),
# or better, use the AWS MCP Server's browser OAuth flow with the console
# password and create no long-lived key at all.

variable "create_agent_identity" {
  type        = bool
  default     = true
  description = "Create the scoped read-only investigation user."
}

resource "aws_iam_user" "agent_ro" {
  count = var.create_agent_identity ? 1 : 0
  name  = "continuityops-agent-ro"

  tags = {
    Purpose  = "cost-and-inventory-investigation"
    ReadOnly = "true"
    Replaces = "root-access-keys"
    BreakFix = "BF-2026-029"
  }
}

resource "aws_iam_policy" "agent_ro" {
  count       = var.create_agent_identity ? 1 : 0
  name        = "ContinuityOpsAgentReadOnly"
  description = "Cost + inventory reads. No mutations. Data-plane reads explicitly denied."

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "CostAndBudgetRead"
        Effect = "Allow"
        Action = [
          "ce:GetCostAndUsage",
          "ce:GetCostAndUsageWithResources",
          "ce:GetCostForecast",
          "ce:GetDimensionValues",
          "ce:GetTags",
          "ce:GetAnomalies",
          "ce:GetAnomalyMonitors",
          "ce:ListCostAllocationTags",
          "cur:DescribeReportDefinitions",
          "budgets:ViewBudget",
          "budgets:DescribeBudgets",
          "billing:GetBillingData",
          "billing:GetBillingDetails",
          "billing:ListBillingViews",
          "account:GetAccountInformation",
        ]
        Resource = "*"
      },
      {
        Sid    = "InventoryReadOnly"
        Effect = "Allow"
        Action = [
          "sts:GetCallerIdentity",
          "ec2:Describe*",
          "eks:List*",
          "eks:Describe*",
          "ecs:List*",
          "ecs:Describe*",
          "elasticloadbalancing:Describe*",
          "autoscaling:Describe*",
          "cloudtrail:DescribeTrails",
          "cloudtrail:GetTrailStatus",
          "cloudtrail:GetEventSelectors",
          "kms:ListKeys",
          "kms:ListAliases",
          "kms:DescribeKey",
          "lambda:ListFunctions",
          "lambda:GetFunctionConfiguration",
          "sqs:ListQueues",
          "sqs:GetQueueAttributes",
          "logs:DescribeLogGroups",
          "ecr:DescribeRepositories",
          "s3:ListAllMyBuckets",
          "s3:GetBucketLocation",
          "s3:GetBucketVersioning",
          "dynamodb:ListTables",
          "dynamodb:DescribeTable",
          "iam:GetAccountSummary",
          "iam:ListRoles",
          "iam:ListAttachedRolePolicies",
        ]
        Resource = "*"
      },
      {
        # Required for the AWS MCP Server's OAuth 2.1 browser sign-in. Without
        # these the flow fails with "Ensure your IAM principal has
        # signin:AuthorizeOAuth2Access and signin:CreateOAuth2Token permissions
        # for your MCP server resource."
        #
        # AuthorizeOAuth2Access = interactive authorization-code sign-in.
        # CreateOAuth2Token     = exchanging that code (or a refresh token) for
        #                         an access token.
        #
        # Scoped to the MCP service principal, not "*", so this grants OAuth
        # sign-in to the MCP server ONLY — not to arbitrary sign-in resources.
        # AWS also publishes AWSMCPSignInOAuthAccessPolicy for this; the inline
        # form is used here to keep the whole grant reviewable in one place.
        #
        # Note this is authentication, not authorization: it lets the identity
        # obtain a session. What that session may DO is still bounded by the
        # Allow/Deny statements above, so the read-only ceiling is unchanged.
        Sid    = "McpServerOAuthSignIn"
        Effect = "Allow"
        Action = [
          "signin:AuthorizeOAuth2Access",
          "signin:CreateOAuth2Token",
        ]
        Resource = "arn:aws:signin:*:*:service-principal/aws-mcp.amazonaws.com"
      },
      {
        # Explicit Deny beats any Allow, including a broader policy attached to
        # this user later. Note that the AWS managed ReadOnlyAccess policy — the
        # obvious shortcut — DOES grant s3:GetObject.
        Sid    = "DenyDataPlaneAndSecrets"
        Effect = "Deny"
        Action = [
          "s3:GetObject",
          "s3:GetObjectVersion",
          "dynamodb:GetItem",
          "dynamodb:Query",
          "dynamodb:Scan",
          "kms:Decrypt",
          "secretsmanager:GetSecretValue",
          "ssm:GetParameter",
          "ssm:GetParameters",
          "logs:GetLogEvents",
          "logs:FilterLogEvents",
        ]
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_user_policy_attachment" "agent_ro" {
  count      = var.create_agent_identity ? 1 : 0
  user       = aws_iam_user.agent_ro[0].name
  policy_arn = aws_iam_policy.agent_ro[0].arn
}

output "agent_identity" {
  value = var.create_agent_identity ? {
    user_name          = aws_iam_user.agent_ro[0].name
    policy_arn         = aws_iam_policy.agent_ro[0].arn
    access_key_created = false
    next_step          = "Mint a key in the console, or use the MCP OAuth flow. Then delete the root access keys."
  } : null
}
