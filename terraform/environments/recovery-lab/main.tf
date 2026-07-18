# Minimal recovery-lab root so GHA OIDC plan can go green before full stack modules land.
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "continuityops"
      Environment = "recovery-lab"
      ManagedBy   = "terraform"
    }
  }
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

check "account_guard" {
  assert {
    condition     = data.aws_caller_identity.current.account_id == var.aws_account_id
    error_message = "Caller account must match var.aws_account_id (ContinuityOps lab)."
  }
}

output "account_id" {
  value = data.aws_caller_identity.current.account_id
}

output "region" {
  value = data.aws_region.current.name
}
