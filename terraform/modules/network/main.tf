# Network composition scaffold for single-account lab (staging / recovery-lab).

variable "environment" {
  type = string
}

variable "cidr_block" {
  type    = string
  default = "10.20.0.0/16"
}

variable "enable_network_resources" {
  type    = bool
  default = false
}

locals {
  private_subnet_cidrs = ["10.20.1.0/24", "10.20.2.0/24"]
  public_subnet_cidrs  = ["10.20.101.0/24", "10.20.102.0/24"]
}

output "network_boundary" {
  value = {
    cidr                 = var.cidr_block
    private_subnet_cidrs = local.private_subnet_cidrs
    public_subnet_cidrs  = local.public_subnet_cidrs
    multi_account        = false
    enable_guard         = var.enable_network_resources
    note                 = "Designed only; not applied (enable_network_resources=false)"
  }
}
