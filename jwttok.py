import jwt
import uuid
import os,sys
import datetime
import yaml
import argparse

def loadConfig(configFile):
    cfg = None
    with open(configFile, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    return cfg


def openFile(fileName):
    data = ""
    with open (fileName, "r") as f:
        data = f.read()
    return data

def createToken(thingId, payload, privateKey):
    return jwt.encode(payload, privateKey, algorithm='RS256', headers={'kid': thingId})

def decodeToken(token, audience, publicKey):
    return jwt.decode(token, publicKey,audience=audience, algorithms='RS256', verify=True)

def main(argv):
    print("make assymetric flashlex token.")

    # Read in command-line parameters
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config", action="store", required=True, dest="config", help="the YAML configuration file")

    args = parser.parse_args()
    config = loadConfig(args.config)

    privateKey = openFile("{0}/{1}".format(
        config['flashlex']['thing']['keys']['path'],
        config['flashlex']['thing']['keys']['privateKey'],
        ))
    publicKey = openFile("{0}/{1}".format(
        config['flashlex']['thing']['keys']['path'],
        config['flashlex']['thing']['keys']['publicKey'],
        ))

    thingId=config["flashlex"]["thing"]["id"]

    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=1200),
        'nbf': datetime.datetime.utcnow(),
        'iss': 'urn:thing:{0}'.format(thingId),
        'aud': 'urn:flashlex:{0}'.format(thingId)
    }

    jwt = createToken(thingId, payload, privateKey)
    print("{0}".format(jwt.decode("utf-8")))
    print(decodeToken(jwt, 'urn:flashlex:{0}'.format(thingId), publicKey))

if __name__ == "__main__":
    main(sys.argv[1:])
