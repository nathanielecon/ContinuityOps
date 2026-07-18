#!/usr/bin/env bash
# Idempotent remote-state bootstrap for ContinuityOps GHA OIDC applies.
# Runs in GitHub Actions as continuityops-gha (not Cursor Cloud Agent).
# Creates S3 state bucket + DynamoDB lock table when missing.
set -euo pipefail

ACCOUNT="$(aws sts get-caller-identity --query Account --output text)"
REGION="${AWS_REGION:-us-east-1}"
BUCKET="${TF_STATE_BUCKET:-continuityops-tfstate-${ACCOUNT}}"
TABLE="${TF_LOCK_TABLE:-continuityops-tf-locks}"

echo "ensure-tfstate account=${ACCOUNT} region=${REGION} bucket=${BUCKET} table=${TABLE}"

if aws s3api head-bucket --bucket "${BUCKET}" 2>/dev/null; then
  echo "bucket exists: ${BUCKET}"
else
  echo "creating bucket: ${BUCKET}"
  if [[ "${REGION}" == "us-east-1" ]]; then
    aws s3api create-bucket --bucket "${BUCKET}" --region "${REGION}"
  else
    aws s3api create-bucket \
      --bucket "${BUCKET}" \
      --region "${REGION}" \
      --create-bucket-configuration "LocationConstraint=${REGION}"
  fi
fi

aws s3api put-bucket-versioning \
  --bucket "${BUCKET}" \
  --versioning-configuration Status=Enabled

aws s3api put-bucket-encryption \
  --bucket "${BUCKET}" \
  --server-side-encryption-configuration \
  '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"},"BucketKeyEnabled":true}]}'

aws s3api put-public-access-block \
  --bucket "${BUCKET}" \
  --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

if aws dynamodb describe-table --table-name "${TABLE}" --region "${REGION}" >/dev/null 2>&1; then
  echo "lock table exists: ${TABLE}"
else
  echo "creating lock table: ${TABLE}"
  aws dynamodb create-table \
    --table-name "${TABLE}" \
    --attribute-definitions AttributeName=LockID,AttributeType=S \
    --key-schema AttributeName=LockID,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region "${REGION}" \
    --tags Key=Project,Value=continuityops Key=ManagedBy,Value=ensure-tfstate
  aws dynamodb wait table-exists --table-name "${TABLE}" --region "${REGION}"
fi

echo "TF_STATE_BUCKET=${BUCKET}"
echo "TF_LOCK_TABLE=${TABLE}"
