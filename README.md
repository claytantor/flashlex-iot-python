# flashlex-pi
the python raspberry pi IOT project for makers yes

# supporting stuff
https://docs.aws.amazon.com/greengrass/latest/developerguide/IoT-SDK.html


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
In order to connect a device, you need to download the following:
A certificate for this thing	fc91e1ff06.cert.pem	Download
A public key	fc91e1ff06.public.key	Download
A private key	fc91e1ff06.private.key	Download

# endpoint

python basicPubSub.py -e a1khvirpxw0646-ats.iot.us-east-1.amazonaws.com -r ssl/AmazonRootCA1.pem -c ../keys/fc91e1ff06-certificate.pem.crt -k ../keys/fc91e1ff06-private.pem.key


## steps
git clone https://github.com/claytantor/flashlex-pi.git
cd flashlex-pi/
pip install virtualenv
/home/pi/.local/bin/virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
