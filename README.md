# flashlex-pi-python

[![Join the chat at https://gitter.im/flashlex-pi-python/community](https://badges.gitter.im/flashlex-pi-python/community.svg)](https://gitter.im/flashlex-pi-python/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![Build Status](https://travis-ci.org/claytantor/flashlex-pi-python.svg?branch=master)](https://travis-ci.org/claytantor/flashlex-pi-python) [![Join the chat at https://gitter.im/flashlex-iot-python/community](https://badges.gitter.im/flashlex-iot-python/community.svg)](https://gitter.im/flashlex-iot-python/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

the python raspberry pi IOT project for makers 

# supporting stuff
* The Python AWS IOT SDK - https://docs.aws.amazon.com/greengrass/latest/developerguide/IoT-SDK.html
* FlashLex Python Community on Gitter - https://gitter.im/flashlex-pi-python/community

# using python 3
you need the ssl system packages because IOT requires ssl

```
python3 -m venv venv --system-site-packages
source venv/bin/activate
python
import ssl
print (ssl.OPENSSL_VERSION)
OpenSSL 1.1.0j  20 Nov 2018
```

# installing AWS IOT on the PI
git clone https://github.com/aws/aws-iot-device-sdk-python.git
cd aws-iot-device-sdk-python/
sudo python setup.py install

# keys
In order to connect a device, you need to download the following a certificate for this thing.
````
<my-iot-id>.cert.pem
A public key	<my-iot-id>.public.key
A private key	<my-iot-id>.private.key
```

# pub sub

```
python basicPubSub.py -e <my-iot-endpoint>.iot.us-east-1.amazonaws.com -r ssl/AmazonRootCA1.pem -c ../keys/<my-iot-id>-certificate.pem.crt -k ../keys/<my-iot-id>-private.pem.key
```


## steps
```
git clone https://github.com/claytantor/flashlex-pi.git
cd flashlex-pi/
pip install virtualenv
/home/pi/.local/bin/virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
