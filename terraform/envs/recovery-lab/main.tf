module "environment" {
  source      = "../../modules/environments"
  environment = "recovery-lab"
  project     = "continuityops"
}

module "iam" {
  source               = "../../modules/iam"
  environment          = "recovery-lab"
  github_repo          = "nathanielecon/ContinuityOps"
  enable_iam_resources = false
}

module "network" {
  source                   = "../../modules/network"
  environment              = "recovery-lab"
  cidr_block               = "10.30.0.0/16"
  enable_network_resources = false
}

output "recovery_lab_tags" {
  value = module.environment.tags
}

output "recovery_lab_cost_drivers" {
  value = module.environment.cost_drivers
}

output "teardown_required" {
  value = module.environment.teardown_required
}
