#!/usr/bin/env bash
# Deploy jsoto.me to Google Cloud Run.
# Edit the variables below, then: bash scripts/gcp-deploy.sh

set -euo pipefail

PROJECT_ID="${GCP_PROJECT_ID:-jsoto-me-site}"
REGION="${GCP_REGION:-us-central1}"
SERVICE_NAME="${GCP_SERVICE_NAME:-jsoto-me}"
REPO_NAME="${GCP_REPO_NAME:-jsoto-site}"
IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${SERVICE_NAME}"

# Your real domain (no https://)
DOMAIN="${SITE_DOMAIN:-jsoto.me}"

if [[ -z "${DJANGO_SECRET_KEY:-}" ]]; then
  echo "Set DJANGO_SECRET_KEY before deploying, e.g.:"
  echo "  export DJANGO_SECRET_KEY=\$(python -c \"import secrets; print(secrets.token_urlsafe(50))\")"
  exit 1
fi

gcloud config set project "${PROJECT_ID}"

gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com

if ! gcloud artifacts repositories describe "${REPO_NAME}" --location="${REGION}" &>/dev/null; then
  gcloud artifacts repositories create "${REPO_NAME}" \
    --repository-format=docker \
    --location="${REGION}"
fi

gcloud builds submit --tag "${IMAGE}"

gcloud run deploy "${SERVICE_NAME}" \
  --image "${IMAGE}" \
  --region "${REGION}" \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "DJANGO_DEBUG=false,DJANGO_ALLOWED_HOSTS=${DOMAIN},www.${DOMAIN},DJANGO_CSRF_TRUSTED_ORIGINS=https://${DOMAIN},https://www.${DOMAIN},DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}"

echo ""
echo "Deployed. Service URL:"
gcloud run services describe "${SERVICE_NAME}" --region "${REGION}" --format='value(status.url)'
echo ""
echo "Next: Cloud Run → ${SERVICE_NAME} → Manage custom domains → add ${DOMAIN} and www.${DOMAIN}"
