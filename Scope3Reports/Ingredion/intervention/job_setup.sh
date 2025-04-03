#!/usr/bin/env bash
set -ex

# Run as: TEST=-test ./job_setup.sh for running a test version. Be sure to add a test suffix to the
# version in the job.yaml file.

IMAGE="473168459077.dkr.ecr.us-west-2.amazonaws.com/carver:20.4.0"
BUCKET="com-cibo-salus-at-scale-alt"

NAMESPACE=$(if [ -z "${TEST}" ]; then echo "carver-workflows"; else echo "carver-workflows-test-smohar"; fi)
NAME=$(cat job.yaml | yq .jobId)
YEAR=$(cat job.yaml | yq .jobYear)
VERSION=$(cat job.yaml | yq .jobVersion)

RUN_TYPE="intervention"
LOCAL_DATA_DIR="/Users/smohar/Development/cibo/my-scripts/Scope3Reports/Ingredion/${RUN_TYPE}"
JOB_PATH="GenericRunner/${YEAR}/${NAME}/${VERSION}"

python3 ../../data_prep/yaml_to_json.py ${LOCAL_DATA_DIR}/job.yaml ${LOCAL_DATA_DIR}/job.json
# Careful! Will delete if the version doesn't update
aws s3 rm --recursive s3://${BUCKET}/${JOB_PATH} --exclude "staging_data_NO_MODS/*"
aws s3 cp ${LOCAL_DATA_DIR}/job.json s3://${BUCKET}/${JOB_PATH}/job.json

# growerdata.json for each boundaryID should be in staging_data_NO_MODS/unprepared_inputs/<boundaryID>
aws s3 cp --recursive s3://com-cibo-salus-at-scale-alt/GenericRunner/2025/ingredion-intervention/staging_data_NO_MODS/ \
                      s3://${BUCKET}/GenericRunner/${YEAR}/${NAME}/${VERSION}/batchmode/

# Note that the growerdata.json must be staged like below, where "argo_il" maps to a boundaryID in the job.yaml: 
# s3://com-cibo-salus-at-scale-alt/GenericRunner/2025/ingredion-intervention/v1-test/batchmode/unprepared_inputs/argo_il/growerdata.json
# s3://com-cibo-salus-at-scale-alt/GenericRunner/2025/ingredion-intervention/v1-test/batchmode/unprepared_inputs/council_bluffs_ia/growerdata.json

argo submit -n ${NAMESPACE} -l user=smohar -l runType=${RUN_TYPE} --from workflowtemplate/carver-job \
  -p jobPath=${JOB_PATH} \
  -p image=${IMAGE} \
  -p s3Bucket=${BUCKET}
