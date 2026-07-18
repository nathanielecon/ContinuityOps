module "environment" {
  source      = "../../modules/environments"
  environment = "staging"
  project     = "continuityops"
}

module "iam" {
  source               = "../../modules/iam"
  environment          = "staging"
  github_repo          = "nathanielecon/ContinuityOps"
  enable_iam_resources = false
}

module "network" {
  source                   = "../../modules/network"
  environment              = "staging"
  enable_network_resources = false
}

# First live AWS object via GHA OIDC → continuityops-gha (not CursorCloudAgent).
# Uses logs:* (already on continuityops-gha lab policy); not SSM.
resource "aws_cloudwatch_log_group" "live_marker" {
  name              = "/continuityops/staging/live-marker"
  retention_in_days = 14

  tags = {
    Purpose = "control-plane-smoke"
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

output "live_marker_log_group" {
  value = aws_cloudwatch_log_group.live_marker.name
}
