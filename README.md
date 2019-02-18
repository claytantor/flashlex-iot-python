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

## steps
git clone https://github.com/claytantor/flashlex-pi.git
cd flashlex-pi/
pip install virtualenv
/home/pi/.local/bin/virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
