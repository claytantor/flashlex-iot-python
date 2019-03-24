#!/bin/bash
# stop script on error
set -e

THING_NAME=$1
THING_ENDPOINT=$2


if [ $(python3 openssl.py) == "true" ]
then

echo OpenSSL is enabled.
echo "thing name: ${THING_NAME} thing endpoint: ${THING_ENDPOINT}"
./venv/bin/python bootstrap.py -e ${THING_ENDPOINT} -r ../root-ca-cert.pem -c ../${THING_NAME}-certificate.pem -k ../${THING_NAME}-keypair-private.pem --mode both --topic pubsub/${THING_NAME}

else
echo ERROR: OpenSSL is required fro IOT TLS.
exit 0
fi
