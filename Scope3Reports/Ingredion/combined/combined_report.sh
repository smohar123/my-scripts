#!/usr/bin/env bash
set -ex

IMAGE="473168459077.dkr.ecr.us-west-2.amazonaws.com/carver:20.4.0"
BUCKET="com-cibo-salus-at-scale-alt"

NAMESPACE="carver-workflows"
NAME="ingredion-supplyshed"
YEAR="2025"
VERSION="v1"
JOB_PATH="GenericRunner/${YEAR}/${NAME}/${VERSION}"
REPORT_NAME=combined
INTERVENTION_RUN_ID="GenericRunner/2025/ingredion-intervention"
aws s3 rm --recursive "s3://${BUCKET}/GenericRunner/${YEAR}/${NAME}/${VERSION}/reports/${REPORT_NAME}" 
argo submit -n ${NAMESPACE} -l customer=${NAME} -l runType=combined --from workflowtemplate/carver-combined-report-job \
  -p s3Bucket=${BUCKET} \
  -p jobPath=${JOB_PATH} \
  -p reportName=${REPORT_NAME} \
  -p image=${IMAGE} \
  -p exclusionRunIds="${INTERVENTION_RUN_ID}"