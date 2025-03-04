#!/usr/bin/env bash
set -ex

# Run as: TEST=1 ./job_setup.sh for running a test version. Be sure to add a test suffix to the
# version in the job.yaml file.

IMAGE="473168459077.dkr.ecr.us-west-2.amazonaws.com/carver:19.5.7"
BUCKET="com-cibo-salus-at-scale-alt"

NAMESPACE=$(if [ -z "${TEST}" ]; then echo "carver-workflows"; else echo "carver-workflows-test-scott"; fi)
NAME=$(cat job.yaml | yq .jobId)
YEAR=$(cat job.yaml | yq .jobYear)
VERSION=$(cat job.yaml | yq .jobVersion)

argo submit -n ${NAMESPACE} -l user=swilson -l runType=supplyshed --from workflowtemplate/combine-reports \
  -p image=${IMAGE} \
  -p baseS3URL="s3://${BUCKET}/GenericRunner/${YEAR}/${NAME}/${VERSION}" \
  -p reportName=default \
  -p overwriteReportFiles=true
