import jwt
import uuid
import os,sys
import datetime
import yaml
import argparse
from flashlexpi.sdk import FlashlexSDK

def load_config(configFile):
    cfg = None
    with open(configFile, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    return cfg


def main(argv):
    print("collect a message.")

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config", action="store", required=True, dest="config", help="the YAML configuration file")

    args = parser.parse_args()
    flashlexSDK = FlashlexSDK(args.config)
    status_code = flashlexSDK.collectMessage({'foo':'bar'})
    print("status code:",status_code)


if __name__ == "__main__":
    main(sys.argv[1:])
