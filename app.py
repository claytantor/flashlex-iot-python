import logging
import argparse
import _thread
import yaml

from flashlex.thread import basicPubSub

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')

LOGGER = logging.getLogger(__name__)


def loadConfig(configFile):
    cfg = None
    with open(configFile, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return cfg


AllowedActions = ['both', 'publish', 'subscribe']

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

# Read in command-line parameters
parser = argparse.ArgumentParser()

parser.add_argument("-c", "--config", action="store", required=True, dest="config", help="the YAML configuration file")

args = parser.parse_args()
config = loadConfig(args.config)

# if args.mode not in AllowedActions:
#     parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(AllowedActions)))
#     exit(2)

if config.thing.useWebsocket and config.thing.keys.certificate and config.thing.keys.privateKey:
    parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
    exit(2)

# @TODO should make a config validation
if not config.thing.useWebsocket and (not config.thing.keys.certificate or not config.thing.keys.privateKey):
    parser.error("Missing credentials for authentication.")
    exit(2)

# Port defaults
if config.thing.useWebsocket and not config.thing.port:  # When no port override for WebSocket, default to 443
    config.thing.port = 443
if not args.useWebsocket and not config.thing.port:  # When no port override for non-WebSocket, default to 8883
    config.thing.port = 8883

# # Configure logging
# logger = logging.getLogger("AWSIoTPythonSDK.core")
# logger.setLevel(logging.DEBUG)
# streamHandler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# streamHandler.setFormatter(formatter)
# logger.addHandler(streamHandler)

# mode = args.mode
# message = args.message

# Create two threads as follows
try:
   _thread.start_new_thread(basicPubSub(
       "Thread-1",
       "This is a basic message.",
        config,
        logging.INFO, 
        customCallback))
except:
   print ("Error: unable to start thread")

while 1:
   pass

