variable "project" {
  type        = string
  description = "Project name prefix"
  default     = "continuityops"
}

variable "environment" {
  type        = string
  description = "Environment key: staging | recovery-lab"
}

variable "aws_region" {
  type        = string
  description = "AWS region for lab resources"
  default     = "us-east-1"
}

variable "state_bucket_name" {
  type        = string
  description = "PLACEHOLDER — replace before apply"
  default     = "PLACEHOLDER_STATE_BUCKET"
}

variable "lock_table_name" {
  type        = string
  description = "PLACEHOLDER DynamoDB lock table"
  default     = "PLACEHOLDER_LOCK_TABLE"
}

variable "github_repo" {
  type        = string
  description = "GitHub repository for OIDC trust (owner/name)"
  default     = "nathanielecon/ContinuityOps"
}

variable "cost_center" {
  type        = string
  description = "Cost allocation tag"
  default     = "lab-portfolio"
}
