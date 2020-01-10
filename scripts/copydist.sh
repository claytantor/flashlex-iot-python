#!/bin/bash

dt_timestamp=$(date +%s)
git_branchname=$(git branch | grep \* | cut -d ' ' -f2)
git_hash=$(git rev-parse --verify HEAD)

bucket_path="s3://github.com.flashlex-iot-python/$SERVERLESS_STAGE/"
file="${REPO}-${TRAVIS_COMMIT}.zip"

aws iam get-user
wget -O "${REPO}-${TRAVIS_COMMIT}.zip" "https://github.com/claytantor/flashlex-iot-python/zipball/${git_branchname}/"
aws s3 cp $file $bucket_path 