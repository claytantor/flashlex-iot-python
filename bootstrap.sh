#!/bin/bash

python3 -m venv venv --system-site-packages
source venv/bin/activate

if [ $(python3 openssl.py) == "true" ]
then
echo OpenSSL is enabled.
pip install -r requirements.txt
else
echo ERROR: OpenSSL is required fro IOT TLS.
exit 0
fi
