#!/usr/bin/env bash
# Read-only account-wide inventory of things that cost money (BF-2026-030).
#
# STRICTLY READ-ONLY: describe/list/get only. No create, modify, or delete.
# Every call is tolerated on failure so a missing permission degrades the report
# rather than aborting it — the OIDC deploy role is Terraform-scoped and may lack
# ce:* or cloudtrail:*.
#
# Answers, without needing an MCP connector:
#   - is cops-staging actually gone at the API level (not just absent from state)?
#   - what is the ~$1.16/day second workload, and which region is it in?
#   - has the EKS line dropped to $0.00/day since the teardown?
set -uo pipefail

REGION_DEFAULT="${AWS_REGION:-us-east-1}"

hr() { printf '\n=== %s ===\n' "$1"; }
try() { "$@" 2>&1 || echo "  (call failed or not permitted: $*)"; }

hr "Identity"
try aws sts get-caller-identity --output table

# ---------------------------------------------------------------------------
# Cost — the falsifiable test of the BF-2026-029 attribution
# ---------------------------------------------------------------------------
hr "Daily cost by service (last 10 days)"
START="$(date -u -d '10 days ago' +%Y-%m-%d)"
END="$(date -u -d 'tomorrow' +%Y-%m-%d)"
echo "window ${START} .. ${END}"
try aws ce get-cost-and-usage \
  --time-period "Start=${START},End=${END}" \
  --granularity DAILY \
  --metrics UnblendedCost \
  --group-by Type=DIMENSION,Key=SERVICE \
  --region us-east-1 \
  --output json

hr "Cost by region (last 10 days) — locates the second workload"
try aws ce get-cost-and-usage \
  --time-period "Start=${START},End=${END}" \
  --granularity MONTHLY \
  --metrics UnblendedCost \
  --group-by Type=DIMENSION,Key=REGION \
  --region us-east-1 \
  --output json

# ---------------------------------------------------------------------------
# Per-region inventory of billable resources
# ---------------------------------------------------------------------------
REGIONS="$(aws ec2 describe-regions --query 'Regions[].RegionName' --output text 2>/dev/null)"
if [[ -z "${REGIONS}" ]]; then
  echo "describe-regions failed; falling back to ${REGION_DEFAULT}"
  REGIONS="${REGION_DEFAULT}"
fi

for r in ${REGIONS}; do
  # Collect first, print only if the region has anything billable. An empty
  # 30-region dump buries the one region that matters.
  out=""
  add() { [[ -n "$2" && "$2" != "None" ]] && out+="  $1: $2"$'\n'; }

  add "eks-clusters"     "$(aws eks list-clusters --region "$r" --query 'clusters[]' --output text 2>/dev/null)"
  add "ecs-clusters"     "$(aws ecs list-clusters --region "$r" --query 'clusterArns[]' --output text 2>/dev/null)"
  add "alb-nlb"          "$(aws elbv2 describe-load-balancers --region "$r" --query 'LoadBalancers[].[LoadBalancerName,Type,VpcId,CreatedTime]' --output text 2>/dev/null)"
  add "classic-elb"      "$(aws elb describe-load-balancers --region "$r" --query 'LoadBalancerDescriptions[].[LoadBalancerName,VPCId]' --output text 2>/dev/null)"
  add "ec2-running"      "$(aws ec2 describe-instances --region "$r" --filters Name=instance-state-name,Values=running --query 'Reservations[].Instances[].[InstanceId,InstanceType,LaunchTime]' --output text 2>/dev/null)"
  add "nat-gateways"     "$(aws ec2 describe-nat-gateways --region "$r" --filter Name=state,Values=available --query 'NatGateways[].NatGatewayId' --output text 2>/dev/null)"
  add "elastic-ips"      "$(aws ec2 describe-addresses --region "$r" --query 'Addresses[].[PublicIp,AssociationId]' --output text 2>/dev/null)"
  add "unattached-ebs"   "$(aws ec2 describe-volumes --region "$r" --filters Name=status,Values=available --query 'Volumes[].[VolumeId,Size]' --output text 2>/dev/null)"
  add "rds"              "$(aws rds describe-db-instances --region "$r" --query 'DBInstances[].[DBInstanceIdentifier,DBInstanceClass]' --output text 2>/dev/null)"
  add "cloudtrail"       "$(aws cloudtrail describe-trails --region "$r" --query 'trailList[].[Name,IsMultiRegionTrail]' --output text 2>/dev/null)"
  add "kms-cmks"         "$(aws kms list-aliases --region "$r" --query 'Aliases[?!starts_with(AliasName, `alias/aws/`)].AliasName' --output text 2>/dev/null)"

  if [[ -n "${out}" ]]; then
    printf '\n--- region %s ---\n%s' "$r" "${out}"
  fi
done

# ---------------------------------------------------------------------------
# ECS detail — the $0.296/day line
# ---------------------------------------------------------------------------
hr "ECS service detail (regions with clusters)"
for r in ${REGIONS}; do
  for c in $(aws ecs list-clusters --region "$r" --query 'clusterArns[]' --output text 2>/dev/null); do
    echo "cluster ${c} (${r})"
    try aws ecs describe-clusters --region "$r" --clusters "$c" \
      --query 'clusters[].[clusterName,status,runningTasksCount,activeServicesCount]' --output text
    for s in $(aws ecs list-services --region "$r" --cluster "$c" --query 'serviceArns[]' --output text 2>/dev/null); do
      try aws ecs describe-services --region "$r" --cluster "$c" --services "$s" \
        --query 'services[].[serviceName,launchType,desiredCount,runningCount]' --output text
    done
  done
done

hr "Global"
try aws s3 ls
try aws budgets describe-budgets --account-id "$(aws sts get-caller-identity --query Account --output text 2>/dev/null)" --output table

echo
echo "Inventory complete. READ-ONLY — nothing was modified or deleted."
