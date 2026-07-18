variable "aws_region" {
  description = "AWS region for recovery-lab drills."
  type        = string
  default     = "us-east-1"
}

variable "aws_account_id" {
  description = "Target AWS account ID for ContinuityOps recovery drills."
  type        = string
  default     = "000000000000"
}
