terraform {
  required_version = ">= 1.5.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "continuityops-tfstate-283077380808"
    key            = "envs/recovery-lab/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "continuityops-tf-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = "us-east-1"

  default_tags {
    tags = {
      Project     = "continuityops"
      Environment = "recovery-lab"
      ManagedBy   = "terraform"
      CostCenter  = "lab-portfolio"
    }
  }
}
