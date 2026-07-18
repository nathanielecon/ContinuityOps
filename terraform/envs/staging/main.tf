module "environment" {
  source      = "../../modules/environments"
  environment = "staging"
  project     = "continuityops"
}

module "iam" {
  source               = "../../modules/iam"
  environment          = "staging"
  github_repo          = "nathanielecon/ContinuityOps"
  aws_account_id       = "283077380808"
  enable_iam_resources = true
}

module "network" {
  source                   = "../../modules/network"
  environment              = "staging"
  enable_network_resources = true
}

module "serverless" {
  source           = "../../modules/serverless"
  environment      = "staging"
  enable_serverless = true
  lambda_role_arn  = module.iam.role_interface.lambda_role_arn
  depends_on       = [module.iam]
}

module "eks" {
  source      = "../../modules/eks"
  environment = "staging"
  enable_eks  = true
  # Public subnets for cost-capped lab (no NAT).
  subnet_ids  = module.network.network_boundary.public_subnet_ids
  depends_on  = [module.network]
}

# Control-plane smoke (already live).
resource "aws_cloudwatch_log_group" "live_marker" {
  name              = "/continuityops/staging/live-marker"
  retention_in_days = 14

  tags = {
    Purpose = "control-plane-smoke"
  }
}

# Lab drill / RTO marker log group (evidence sink for timed restore drills).
resource "aws_cloudwatch_log_group" "drill_rto" {
  name              = "/continuityops/staging/lab-drill-rto"
  retention_in_days = 30

  tags = {
    Purpose = "lab-drill-rto"
  }
}

output "staging_tags" {
  value = module.environment.tags
}

output "staging_iam" {
  value = module.iam.role_interface
}

output "staging_network" {
  value = module.network.network_boundary
}

output "staging_serverless" {
  value = {
    enabled      = module.serverless.serverless_enabled
    queue_url    = module.serverless.queue_url
    lambda_name  = module.serverless.lambda_function_name
  }
}

output "staging_eks" {
  value = {
    enabled  = module.eks.eks_enabled
    name     = module.eks.cluster_name
    endpoint = module.eks.cluster_endpoint
    arn      = module.eks.cluster_arn
  }
}

output "live_marker_log_group" {
  value = aws_cloudwatch_log_group.live_marker.name
}

output "lab_drill_rto_log_group" {
  value = aws_cloudwatch_log_group.drill_rto.name
}
