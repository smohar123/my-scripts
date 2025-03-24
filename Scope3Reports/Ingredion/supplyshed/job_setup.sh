#!/usr/bin/env bash
set -ex

# Run as: TEST=1 ./job_setup.sh for running a test version. Be sure to add a test suffix to the
# version in the job.yaml file.

IMAGE="473168459077.dkr.ecr.us-west-2.amazonaws.com/carver:20.4.0"
BUCKET="com-cibo-salus-at-scale-alt"

NAMESPACE=$(if [ -z "${TEST}" ]; then echo "carver-workflows"; else echo "carver-workflows-test-smohar"; fi)
NAME=$(cat job.yaml | yq .jobId)
YEAR=$(cat job.yaml | yq .jobYear)
VERSION=$(cat job.yaml | yq .jobVersion)

DATA_DIR="/Users/smohar/Development/cibo/my-scripts/Scope3Reports/Ingredion/supplyshed"

python3 ../../data_prep/yaml_to_json.py $DATA_DIR/job.yaml $DATA_DIR/job.json
aws s3 rm --recursive s3://${BUCKET}/GenericRunner/${YEAR}/${NAME}/${VERSION}
aws s3 cp $DATA_DIR/job.json s3://${BUCKET}/GenericRunner/${YEAR}/${NAME}/${VERSION}/job.json

argo submit -n ${NAMESPACE} -l user=smohar -l runType=supplyshed --from workflowtemplate/carver-job \
  -p jobPath=GenericRunner/${YEAR}/${NAME}/${VERSION} \
  -p image=${IMAGE} \
  -p s3Bucket=${BUCKET}
