import logging
import argparse
import _thread
import yaml
import time, threading
import json
import os, sys, traceback
from os.path import dirname, abspath

from flashlexiot.backend.thread import BasicPubsubThread, ExpireMessagesThread, threadTypeFactory
from flashlexiot.backend.callbacks import callbackFactory

from flashlexiot.sdk import FlashlexSDK

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')

LOGGER = logging.getLogger(__name__)

def loadConfig(configFile):
    cfg = None
    with open(configFile, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    return cfg

def main(argv):
    data = sys.stdin.read()

    # Read in command-line parameters
    parser = argparse.ArgumentParser()

    #get defaults for data and keys
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = dirname(dirname(abspath(__file__)))

    parser.add_argument("-c", "--config", action="store", 
        required=True, dest="config", help="the YAML configuration file")
    parser.add_argument("-k", "--keys", action="store", 
        required=False, dest="keys", default="{0}".format(parent_dir), 
        help="the directory path for keys")

    args = parser.parse_args()
    config = loadConfig(args.config)

    #use command args for config overrides
    config["flashlex"]["thing"]["keys"]["path"] = args.keys

    # now send a message to the collector
    flashlexSDK = FlashlexSDK(config)
    status_code = flashlexSDK.collectMessage(json.loads(data))
    print("FlashlexSDK Collector Status Code:",status_code)

if __name__ == "__main__":
    main(sys.argv[1:])

