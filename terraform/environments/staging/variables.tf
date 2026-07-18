variable "aws_region" {
  description = "AWS region for the staging lab."
  type        = string
  default     = "us-east-1"
}

variable "aws_account_id" {
  description = "Target AWS account ID for ContinuityOps lab."
  type        = string
  default     = "000000000000"
}
