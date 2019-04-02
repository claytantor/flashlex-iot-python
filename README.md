# flashlex-pi-python

[![Join the chat at https://gitter.im/flashlex-pi-python/community](https://badges.gitter.im/flashlex-pi-python/community.svg)](https://gitter.im/flashlex-pi-python/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![Build Status](https://travis-ci.org/claytantor/flashlex-pi-python.svg?branch=master)](https://travis-ci.org/claytantor/flashlex-pi-python)

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
```
git clone https://github.com/claytantor/flashlex-pi-python.git
cd flashlex-pi-python
sudo python setup.py install
```

# keys
In order to connect a device, you need to download the following a certificate for this thing.

```
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

# creating the systemd service
Instructions for setting up your service can be found at https://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/

```
sudo cp flashlex.service /lib/systemd/system/flashlex.service
sudo chmod 644 /lib/systemd/system/flashlex.service
sudo systemctl daemon-reload
sudo systemctl enable flashlex.service
```

## add logging to syslog

Then, assuming your distribution is using rsyslog to manage syslogs, create a file in `/etc/rsyslog.d/<new_file>.conf` with the following content:

```
if $programname == '<your program identifier>' then /path/to/log/file.log
& stop
```

restart rsyslog (sudo systemctl restart rsyslog) and enjoy! Your program stdout/stderr will still be available through journalctl (sudo journalctl -u <your program identifier>) but they will also be available in your file of choice.

```
sudo cp flashlex.conf /etc/rsyslog.d/flashlex.conf
sudo systemctl daemon-reload
sudo systemctl restart flashlex.service
sudo systemctl restart rsyslog
```

## check the status of the service
```
sudo systemctl status flashlex.service
```

## rotating logs for your service
you will want to rotate logs so your disk doesnt fill up with logs. your conf file for logrotation looks like this in `/etc/logrotate.conf`:

```
/var/log/flashlex.log {
    daily
    missingok
    rotate 7
    maxage 7
    dateext
    dateyesterday
}
```

make a crontab that executes logrotate daily

```
/usr/sbin/logrotate /etc/logrotate.conf
```

