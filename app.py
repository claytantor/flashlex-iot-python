import logging
import argparse
import _thread
import yaml

from flashlex.thread import basicPubSub
from flashlex.callbacks import factory

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')

LOGGER = logging.getLogger(__name__)

def loadConfig(configFile):
    cfg = None
    with open(configFile, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return cfg

# Read in command-line parameters
parser = argparse.ArgumentParser()

parser.add_argument("-c", "--config", action="store", required=True, dest="config", help="the YAML configuration file")

args = parser.parse_args()
config = loadConfig(args.config)
# print(config)

if config["thing"]["useWebsocket"] and config["thing"]["keys"]["cert"] and config["thing"]["keys"]["privateKey"]:
    print("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
    exit(2)

# @TODO should make a config validation
if not config["thing"]["useWebsocket"] and (not config["thing"]["keys"]["cert"] or not config["thing"]["keys"]["privateKey"]):
    print("Missing credentials for authentication.")
    exit(2)

# Port defaults
if config["thing"]["useWebsocket"] and not config["thing"]["port"]:  # When no port override for WebSocket, default to 443
    config["thing"]["port"] = 443
if not config["thing"]["useWebsocket"] and not config["thing"]["port"]:  # When no port override for non-WebSocket, default to 8883
    config["thing"]["port"] = 8883

# Create two threads as follows
try:
   _thread.start_new_thread(basicPubSub(
       "Thread-1",
       "This is a basic message.",
        config,
        logging.INFO, 
        factory.get_callback_for_config(config).handleMessage))
except:
   print ("Error: unable to start thread")

while 1:
   pass

