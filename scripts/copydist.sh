#!/bin/bash

dt_timestamp=$(date +%s)
zipball="master"
DIST_STAGE="dev"

if [ -n "$CIRCLE_TAG" ]
then
    zipball=$CIRCLE_TAG
elif [ -n "$CIRCLE_BRANCH" ]
then
    zipball=$CIRCLE_BRANCH
    if [[ ${CIRCLE_BRANCH} == "master" ]]; then
        DIST_STAGE="prd"
    fi
fi

bucket_path="s3://github.com.flashlex-iot-python/$DIST_STAGE/"
file="flashlex-iot-python-${CIRCLE_SHA1}.zip"

aws iam get-user
wget -O "flashlex-iot-python-${CIRCLE_SHA1}.zip" "https://github.com/claytantor/flashlex-iot-python/zipball/${zipball}/"
echo "aws s3 cp ${file} ${bucket_path}"
aws s3 cp ${file} ${bucket_path} 