#!/usr/bin/env bash
set -ex

IMAGE="473168459077.dkr.ecr.us-west-2.amazonaws.com/carver:20.0.1"
BUCKET="com-cibo-salus-at-scale-alt"

NAMESPACE=$(if [ -z "${TEST}" ]; then echo "carver-workflows"; else echo "carver-workflows-test-scott"; fi)
NAME=$(cat job.yaml | yq .jobId)
YEAR=$(cat job.yaml | yq .jobYear)
VERSION=$(cat job.yaml | yq .jobVersion)
REPORT_NAME=combined

# aws s3 rm --recursive "s3://${BUCKET}/GenericRunner/${YEAR}/${NAME}/${VERSION}/reports/${REPORT_NAME}" 
argo submit -n ${NAMESPACE} -l user=swilson -l runType=combined --from workflowtemplate/carver-combined-report-job \
  -p s3Bucket=${BUCKET} \
  -p jobPath="GenericRunner/${YEAR}/${NAME}/${VERSION}" \
  -p reportName=${REPORT_NAME} \
  -p image=${IMAGE} \
  -p exclusionRunIds="GenericRunner/2024/nestle-syndicated-programs/v6"
