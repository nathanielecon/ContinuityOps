#!/usr/bin/env bash
# Idempotent remote-state bootstrap for ContinuityOps GHA OIDC applies.
# Runs in GitHub Actions as continuityops-gha (not Cursor Cloud Agent).
# Creates S3 state bucket + DynamoDB lock table when missing.
# Tolerates concurrent create races (BF: apply 29643490577 DynamoDB ResourceInUseException).
set -euo pipefail

ACCOUNT="$(aws sts get-caller-identity --query Account --output text)"
REGION="${AWS_REGION:-us-east-1}"
BUCKET="${TF_STATE_BUCKET:-continuityops-tfstate-${ACCOUNT}}"
TABLE="${TF_LOCK_TABLE:-continuityops-tf-locks}"

echo "ensure-tfstate account=${ACCOUNT} region=${REGION} bucket=${BUCKET} table=${TABLE}"

ensure_bucket() {
  if aws s3api head-bucket --bucket "${BUCKET}" 2>/dev/null; then
    echo "bucket exists: ${BUCKET}"
    return 0
  fi
  echo "creating bucket: ${BUCKET}"
  set +e
  if [[ "${REGION}" == "us-east-1" ]]; then
    out="$(aws s3api create-bucket --bucket "${BUCKET}" --region "${REGION}" 2>&1)"
  else
    out="$(aws s3api create-bucket \
      --bucket "${BUCKET}" \
      --region "${REGION}" \
      --create-bucket-configuration "LocationConstraint=${REGION}" 2>&1)"
  fi
  rc=$?
  set -e
  if [[ $rc -ne 0 ]]; then
    if [[ "${out}" == *"BucketAlreadyOwnedByYou"* ]] || [[ "${out}" == *"BucketAlreadyExists"* ]]; then
      echo "bucket create raced; treating as exists: ${BUCKET}"
    else
      echo "${out}" >&2
      return "$rc"
    fi
  fi
}

ensure_lock_table() {
  if aws dynamodb describe-table --table-name "${TABLE}" --region "${REGION}" >/dev/null 2>&1; then
    echo "lock table exists: ${TABLE}"
    aws dynamodb wait table-exists --table-name "${TABLE}" --region "${REGION}"
    return 0
  fi
  echo "creating lock table: ${TABLE}"
  set +e
  out="$(aws dynamodb create-table \
    --table-name "${TABLE}" \
    --attribute-definitions AttributeName=LockID,AttributeType=S \
    --key-schema AttributeName=LockID,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region "${REGION}" \
    --tags Key=Project,Value=continuityops Key=ManagedBy,Value=ensure-tfstate 2>&1)"
  rc=$?
  set -e
  if [[ $rc -ne 0 ]]; then
    if [[ "${out}" == *"ResourceInUseException"* ]]; then
      echo "lock table create raced; waiting for active: ${TABLE}"
    else
      echo "${out}" >&2
      return "$rc"
    fi
  fi
  aws dynamodb wait table-exists --table-name "${TABLE}" --region "${REGION}"
  echo "lock table ready: ${TABLE}"
}

ensure_bucket

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

ensure_lock_table

echo "TF_STATE_BUCKET=${BUCKET}"
echo "TF_LOCK_TABLE=${TABLE}"
