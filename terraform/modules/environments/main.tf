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
  }

  cost_drivers = [
    "nat_gateway",
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
