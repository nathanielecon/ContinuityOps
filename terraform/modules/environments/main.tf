variable "environment" {
  type = string
  validation {
    condition     = contains(["staging", "recovery-lab"], var.environment)
    error_message = "environment must be staging or recovery-lab"
  }
}

variable "project" {
  type    = string
  default = "continuityops"
}

variable "cost_center" {
  type    = string
  default = "lab-portfolio"
}

locals {
  common_tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "terraform"
    CostCenter  = var.cost_center

    # Machine-readable teardown expectation (BF-2026-029). `teardown_required`
    # was an output nothing consumed; as a tag it is queryable from the console
    # and from Cost Explorer's tag grouping, so "should this still exist?" has an
    # answer that does not depend on anyone remembering.
    #
    # Deliberately a static policy string, not a timestamp: a timestamp()-derived
    # tag changes on every plan and produces perpetual spurious diffs.
    TeardownPolicy = "nightly-scheduled"
    Ephemeral      = "true"
  }

  cost_drivers = [
    "nat_gateway",
    # 1.32 billed extended support at $0.60/hr — 6x standard — for 491.7 hours
    # (BF-2026-029). Guarded by scripts/ci/assert-eks-standard-support.mjs.
    "eks_control_plane_extended_support_rate",
    "eks_control_plane_later_phase",
    "cloudwatch_retention",
    "state_bucket_versioning"
  ]
}

output "tags" {
  value = local.common_tags
}

output "cost_drivers" {
  value = local.cost_drivers
}

output "teardown_required" {
  value = true
}
