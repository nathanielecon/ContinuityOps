# Remote state backend placeholders (do not apply with PLACEHOLDER_* values).
#
# Intended properties:
# - S3 bucket: versioning + SSE + public access block
# - DynamoDB table: LockID for state locking
# - Separate key prefixes per environment

terraform {
  # Backend block is intentionally commented until real names exist.
  # backend "s3" {
  #   bucket         = "REPLACE_ME"
  #   key            = "continuityops/ENV/terraform.tfstate"
  #   region         = "us-east-1"
  #   encrypt        = true
  #   dynamodb_table = "REPLACE_ME"
  # }
}

resource "aws_s3_bucket" "state" {
  count  = var.enable_state_resources ? 1 : 0
  bucket = var.state_bucket_name

  tags = {
    Project     = var.project
    Environment = "shared"
    ManagedBy   = "terraform"
    Purpose     = "remote-state"
  }
}

variable "enable_state_resources" {
  type        = bool
  description = "Guard: keep false until bucket name is approved"
  default     = false
}

variable "project" {
  type    = string
  default = "continuityops"
}

variable "state_bucket_name" {
  type = string
}

variable "lock_table_name" {
  type = string
}

output "state_isolation_notes" {
  value = {
    versioning_required = true
    encryption_required = true
    locking_required    = true
    enable_guard        = var.enable_state_resources
  }
}
