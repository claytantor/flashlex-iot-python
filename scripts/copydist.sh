#!/bin/bash

dt_timestamp=$(date +%s)

bucket_path="s3://github.com.flashlex-iot-python/$SERVERLESS_STAGE/"
file="${REPO}-${CIRCLE_SHA1}.zip"

aws iam get-user
wget -O "${REPO}-${CIRCLE_SHA1}.zip" "https://github.com/claytantor/flashlex-iot-python/zipball/${CIRCLECI_BRANCH}/"
aws s3 cp $file $bucket_path 