#!/usr/bin/env bash
# Safe teardown: Project C staging (options 2+3) + Project A duplicate CloudTrail.
#
# WHY A SCRIPT AND NOT `terraform destroy`:
# Neither stack's state is reachable from a clone. Project C's .gitignore excludes
# infra/terraform/*.tfstate; platform/sandbox/aws-proof has no backend block and no
# committed state. A `terraform destroy` from a fresh checkout finds EMPTY state,
# destroys nothing, and exits 0 — success with no effect. If you still hold the
# original .tfstate on the machine that applied these, prefer terraform destroy
# there; it keeps state and reality in agreement. Use this script otherwise.
#
# DRY RUN BY DEFAULT. Nothing is deleted until you pass --apply.
#
#   ./teardown-2-3-trail.sh            # discover + print the plan, change nothing
#   ./teardown-2-3-trail.sh --apply    # execute
#
# NOT IN SCOPE, deliberately — each is a separate decision with its own risk:
#   * KMS key alias/project-a-sandbox-audit   -> 7-30 day irreversible waiting period
#   * S3 bucket project-a-sandbox-archive-*   -> contains audit log data
#   * AWS Config recorder project-a-sandbox-config
#   * ECR repository                          -> holds the pinned image; required to rebuild
#   * VPC, subnets, CloudWatch log groups     -> no meaningful cost
set -uo pipefail

REGION="${AWS_REGION:-us-east-1}"
APPLY=0
[[ "${1:-}" == "--apply" ]] && APPLY=1

CLUSTER="project-c-staging"
SERVICE="project-c-delivery-api"
LB_NAME="project-c-stg"
DUP_TRAIL="project-a-sandbox-trail"
KEEP_TRAIL="project-a-lzlab-trail"

say()  { printf '\n\033[1m== %s\033[0m\n' "$*"; }
run()  {
  if [[ $APPLY -eq 1 ]]; then
    echo "+ $*"; "$@"
  else
    echo "  [dry-run] $*"
  fi
}
die() { echo "FATAL: $*" >&2; exit 1; }

aws sts get-caller-identity --query Arn --output text >/dev/null 2>&1 \
  || die "no usable AWS credentials"
say "Identity"
aws sts get-caller-identity --output table

# ---------------------------------------------------------------------------
# Discovery — resolve every ARN before touching anything
# ---------------------------------------------------------------------------
say "Discovery"

LB_ARN="$(aws elbv2 describe-load-balancers --names "$LB_NAME" --region "$REGION" \
  --query 'LoadBalancers[0].LoadBalancerArn' --output text 2>/dev/null || echo NONE)"
echo "ALB              : $LB_ARN"

if [[ "$LB_ARN" != "NONE" ]]; then
  LB_SGS="$(aws elbv2 describe-load-balancers --load-balancer-arns "$LB_ARN" --region "$REGION" \
    --query 'LoadBalancers[0].SecurityGroups' --output text)"
  LISTENERS="$(aws elbv2 describe-listeners --load-balancer-arn "$LB_ARN" --region "$REGION" \
    --query 'Listeners[].ListenerArn' --output text)"
  echo "ALB SGs          : ${LB_SGS:-none}"
  echo "Listeners        : ${LISTENERS:-none}"
fi

# Target groups resolved by name prefix, NOT by LB association: once the LB is
# deleted the association is gone and an unassociated group would be orphaned.
TGS="$(aws elbv2 describe-target-groups --region "$REGION" \
  --query "TargetGroups[?starts_with(TargetGroupName, 'project-c')].TargetGroupArn" \
  --output text 2>/dev/null || true)"
echo "Target groups    : ${TGS:-none}"

SVC_STATUS="$(aws ecs describe-services --cluster "$CLUSTER" --services "$SERVICE" --region "$REGION" \
  --query 'services[0].[status,desiredCount,runningCount]' --output text 2>/dev/null || echo NONE)"
echo "ECS service      : $SVC_STATUS"

TRAIL_DUP="$(aws cloudtrail describe-trails --trail-name-list "$DUP_TRAIL" --region "$REGION" \
  --query 'trailList[0].TrailARN' --output text 2>/dev/null || echo NONE)"
TRAIL_KEEP="$(aws cloudtrail describe-trails --trail-name-list "$KEEP_TRAIL" --region "$REGION" \
  --query 'trailList[0].TrailARN' --output text 2>/dev/null || echo NONE)"
echo "Trail to delete  : $TRAIL_DUP"
echo "Trail to KEEP    : $TRAIL_KEEP"

# Refuse to proceed if the surviving trail is missing — never leave the account
# with zero audit coverage.
[[ "$TRAIL_KEEP" == "NONE" ]] && die "$KEEP_TRAIL not found; refusing to delete the only trail"

if [[ $APPLY -eq 0 ]]; then
  cat <<'PLAN'

== Plan (dependency order) ==
  1. ECS service desiredCount -> 0, wait for runningCount 0   (frees the task's public IPv4)
  2. Delete ECS service
  3. Delete ALB                                               (listeners go with it; frees 2 public IPv4)
  4. Wait for ALB deletion to release its ENIs
  5. Delete target group(s)                                   (must follow ALB deletion)
  6. Delete ECS cluster                                       (cosmetic; costs nothing)
  7. Stop logging + delete the duplicate CloudTrail trail
  8. Delete the ALB security group                            (only after ENIs release)

Expected saving ~= $0.836/day ALB+Fargate, plus $0.36/day public IPv4,
plus most of $0.222/day CloudTrail  ==>  roughly $36/month.

Re-run with --apply to execute.
PLAN
  exit 0
fi

# ---------------------------------------------------------------------------
# 1-2. ECS service
# ---------------------------------------------------------------------------
if [[ "$SVC_STATUS" != "NONE" ]]; then
  say "Draining ECS service"
  run aws ecs update-service --cluster "$CLUSTER" --service "$SERVICE" \
    --desired-count 0 --region "$REGION" --no-cli-pager --query 'service.desiredCount'

  echo "waiting for tasks to stop..."
  for i in $(seq 1 30); do
    n="$(aws ecs describe-services --cluster "$CLUSTER" --services "$SERVICE" --region "$REGION" \
      --query 'services[0].runningCount' --output text)"
    echo "  runningCount=$n"
    [[ "$n" == "0" ]] && break
    sleep 10
  done

  say "Deleting ECS service"
  run aws ecs delete-service --cluster "$CLUSTER" --service "$SERVICE" --force \
    --region "$REGION" --no-cli-pager --query 'service.status'
fi

# ---------------------------------------------------------------------------
# 3-5. Load balancer, then target groups
# ---------------------------------------------------------------------------
if [[ "$LB_ARN" != "NONE" ]]; then
  say "Deleting ALB (listeners are removed with it)"
  run aws elbv2 delete-load-balancer --load-balancer-arn "$LB_ARN" --region "$REGION"

  echo "waiting for the load balancer to disappear (ENIs release with it)..."
  if [[ $APPLY -eq 1 ]]; then
    aws elbv2 wait load-balancers-deleted --load-balancer-arns "$LB_ARN" --region "$REGION" \
      && echo "  deleted" || echo "  waiter timed out — verify by hand before deleting SGs"
  fi
fi

for tg in ${TGS:-}; do
  say "Deleting target group $tg"
  run aws elbv2 delete-target-group --target-group-arn "$tg" --region "$REGION"
done

# ---------------------------------------------------------------------------
# 6. Cluster (no cost; keeps the console tidy)
# ---------------------------------------------------------------------------
say "Deleting ECS cluster"
run aws ecs delete-cluster --cluster "$CLUSTER" --region "$REGION" --no-cli-pager --query 'cluster.status'

# ---------------------------------------------------------------------------
# 7. Duplicate CloudTrail
# ---------------------------------------------------------------------------
if [[ "$TRAIL_DUP" != "NONE" ]]; then
  say "Stopping and deleting duplicate trail $DUP_TRAIL"
  run aws cloudtrail stop-logging --name "$DUP_TRAIL" --region "$REGION"
  run aws cloudtrail delete-trail --name "$DUP_TRAIL" --region "$REGION"
  echo "NOTE: its S3 archive bucket and KMS key are deliberately left in place."
fi

# ---------------------------------------------------------------------------
# 8. ALB security group — last, and best-effort
# ---------------------------------------------------------------------------
for sg in ${LB_SGS:-}; do
  [[ "$sg" == "None" ]] && continue
  say "Deleting ALB security group $sg (best effort — ENI release can lag)"
  if [[ $APPLY -eq 1 ]]; then
    aws ec2 delete-security-group --group-id "$sg" --region "$REGION" 2>&1 \
      || echo "  still in use; retry in a few minutes. Harmless: SGs cost nothing."
  else
    echo "  [dry-run] delete-security-group $sg"
  fi
done

# ---------------------------------------------------------------------------
say "Post-teardown verification"
echo "ALBs      : $(aws elbv2 describe-load-balancers --region "$REGION" --query 'LoadBalancers[].LoadBalancerName' --output text)"
echo "ECS       : $(aws ecs list-clusters --region "$REGION" --query 'clusterArns[]' --output text)"
echo "Trails    : $(aws cloudtrail describe-trails --region "$REGION" --query 'trailList[].Name' --output text)"
cat <<'DONE'

Confirm the money actually stopped, 2-3 days out (Cost Explorer lags ~1 day):

  aws ce get-cost-and-usage --time-period Start=<today>,End=<today+2> \
    --granularity DAILY --metrics UnblendedCost \
    --group-by Type=DIMENSION,Key=SERVICE --region us-east-1

Expect: Elastic Load Balancing -> $0.00, Elastic Container Service -> $0.00,
Virtual Private Cloud down by ~$0.36/day, CloudTrail roughly halved.
A reduced-but-nonzero line means something survived.

Rebuilding Project C: the container image is pinned by digest and the ECR
repository was NOT deleted, so `terraform apply` in Project C's infra/terraform
recreates the stack. Only the ALB hostname changes.
DONE
