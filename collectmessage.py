import logging
import argparse
import _thread
import yaml
import time, threading
import os, sys, traceback
from os.path import dirname, abspath

from flashlexpi.backend.thread import BasicPubsubThread, ExpireMessagesThread, threadTypeFactory
from flashlexpi.backend.callbacks import callbackFactory

from flashlexpi.sdk import FlashlexSDK

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')

LOGGER = logging.getLogger(__name__)

def loadConfig(configFile):
    cfg = None
    with open(configFile, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    return cfg

def main(argv):
    print("starting flashelex app.")

    # Read in command-line parameters
    parser = argparse.ArgumentParser()

    #get defaults for data and keys
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = dirname(dirname(abspath(__file__)))

    parser.add_argument("-c", "--config", action="store", 
        required=True, dest="config", help="the YAML configuration file")
    parser.add_argument("-d", "--data", action="store", 
        required=False, dest="data", default="{0}/data".format(dir_path), 
        help="the directory path for thing message data storage")
    parser.add_argument("-k", "--keys", action="store", 
        required=False, dest="keys", default="{0}".format(parent_dir), 
        help="the directory path for keys")

    args = parser.parse_args()
    config = loadConfig(args.config)

    #use command args for config overrides
    config["flashlex"]["app"]["db"]["path"] = args.data
    config["flashlex"]["thing"]["keys"]["path"] = args.keys
    config["flashlex"]["app"]["callback"] = "test"
    config["flashlex"]["app"]["thread"] = "test"
    config["flashlex"]["app"]["loopCount"] = 10

    if config["flashlex"]["thing"]["mqtt"]["useWebsocket"] and config["flashlex"]["thing"]["keys"]["cert"] and config["flashlex"]["thing"]["keys"]["privateKey"]:
        print("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
        exit(2)

    # @TODO should make a config validation
    if not config["flashlex"]["thing"]["mqtt"]["useWebsocket"] and (not config["flashlex"]["thing"]["keys"]["cert"] or not config["flashlex"]["thing"]["keys"]["privateKey"]):
        print("Missing credentials for authentication.")
        exit(2)

    # Port defaults
    if config["flashlex"]["thing"]["mqtt"]["useWebsocket"] and not config["flashlex"]["thing"]["mqtt"]["port"]:  # When no port override for WebSocket, default to 443
        config["flashlex"]["thing"]["mqtt"]["port"] = 443
    if not config["flashlex"]["thing"]["mqtt"]["useWebsocket"] and not config["flashlex"]["thing"]["mqtt"]["port"]:  # When no port override for non-WebSocket, default to 8883
        config["flashlex"]["thing"]["mqtt"]["port"] = 8883

    # now send a message to the collector
    flashlexSDK = FlashlexSDK(config)
    status_code = flashlexSDK.collectMessage({'foo':'bar'})
    print("FlashlexSDK Collector Status Code:",status_code)

if __name__ == "__main__":
    main(sys.argv[1:])

