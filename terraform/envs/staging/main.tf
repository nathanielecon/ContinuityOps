module "environment" {
  source      = "../../modules/environments"
  environment = "staging"
  project     = "continuityops"
}

module "iam" {
  source       = "../../modules/iam"
  environment  = "staging"
  github_repo  = "nathanielecon/ContinuityOps"
  enable_iam_resources = false
}

module "network" {
  source                   = "../../modules/network"
  environment              = "staging"
  enable_network_resources = false
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
