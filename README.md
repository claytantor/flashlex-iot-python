# flashlex-iot-python
the python raspberry pi IOT project for makers 

[![Join the chat at https://gitter.im/flashlex-iot-python/community](https://badges.gitter.im/flashlex-iot-python/community.svg)](https://gitter.im/flashlex-iot-python/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/claytantor/flashlex-iot-python.svg?branch=master)](https://travis-ci.org/claytantor/flashlex-iot-python)



# supporting stuff
* The Python AWS IOT SDK - https://docs.aws.amazon.com/greengrass/latest/developerguide/IoT-SDK.html
* FlashLex Python Community on Gitter - https://gitter.im/flashlex-iot-python/community

# using python 3
you need the ssl system packages because IOT requires ssl

```
python3 -m venv venv --system-site-packages
source venv/bin/activate
python3 -m pip install --user --upgrade pip
python3 -m pip install -r requirements.txt
python3
import ssl
print (ssl.OPENSSL_VERSION)
OpenSSL 1.1.0j  20 Nov 2018
```

# installing AWS IOT on the PI
```
git clone https://github.com/claytantor/flashlex-iot-python.git
cd flashlex-iot-python
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

# bootstrap
python -u bootstrap.py -c keys/config-bootstrap.yml -d $(pwd)/data -k $(pwd)/keys

#collect a message
```
$ source venv/bin/activate
(venv) $ python -u collectmessage.py -c keys/config-bootstrap.yml -d $(pwd)/data -k $(pwd)/keys
starting flashelex app.
collecting message from thing:a44d80ec-bc2d-44d2-8568-eb23f7d44021
https://u100den7gk.execute-api.us-east-1.amazonaws.com/dev/things/a44d80ec-bc2d-44d2-8568-eb23f7d44021/collect {'foo': 'bar'} {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImE0NGQ4MGVjLWJjMmQtNDRkMi04NTY4LWViMjNmN2Q0NDAyMSJ9.eyJleHAiOjE1NTU3NzU5ODMsIm5iZiI6MTU1NTc3NTg2MywiaXNzIjoidXJuOnRoaW5nOmE0NGQ4MGVjLWJjMmQtNDRkMi04NTY4LWViMjNmN2Q0NDAyMSIsImF1ZCI6InVybjpmbGFzaGxleDphNDRkODBlYy1iYzJkLTQ0ZDItODU2OC1lYjIzZjdkNDQwMjEifQ.Thv2m04Bhgqe5T7KkxGgW0ESvW4gATUhRGedzaTOul820CgQCtXlT158X6T-ysoMqTP5N1du2TF3-tY_zU_QPM-K8uTlkqspIBri72aUurl7nOTKpmlxexHaiJlM3BlkZJBIX0T4bnTraCrrc4BscNQRs7jJcWkW277F-ok59fRRYAVa2nZdZVcrI9ZeGUR3a9BrlO4YslYaldLN61YU-Q-Fg4OK3xEcooPUhNNGfEpL0Gpme3dBI123ADwn10jK8snhIBD76kOeoHy2yCD7lYufclwuXeuvl0xA3QAFdZC-GVaywb9AaNPFg1clbGqmfBkl1hIpUDWK4IodqhZ_Zg', 'Content-Type': 'application/json'}
```
