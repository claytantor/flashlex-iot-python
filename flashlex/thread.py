from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import logging
import sys, traceback


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')

LOGGER = logging.getLogger(__name__)

def subscribe(
    config,
    logLevel,
    customCallback):
    """ save messages subscribed to to 
    local database
    """

    topic="ingress/{0}".format(config["thing"]["name"])

    # init LOGGER
    if (logLevel == None):
        logLevel = logging.INFO
    logging.basicConfig(level=logLevel, format=LOG_FORMAT)

    # Init AWSIoTMQTTClient
    myAWSIoTMQTTClient = setupClient(
        config["thing"]["name"], 
        config["thing"]["endpoint"], 
        config["thing"]["port"], 
        "{0}/{1}".format(config["thing"]["keys"]["path"], config["thing"]["keys"]["rootCA"]), #rootca
        "{0}/{1}".format(config["thing"]["keys"]["path"], config["thing"]["keys"]["privateKey"]), #private key
        "{0}/{1}".format(config["thing"]["keys"]["path"], config["thing"]["keys"]["cert"]), #cert 
        config["thing"]["useWebsocket"])

    # Connect and subscribe to AWS IoT
    myAWSIoTMQTTClient.connect()
    myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
    time.sleep(2)    

    loop = True
    while loop:
        LOGGER.debug("subscribe-{0} listening to topic: {1}".format(config["thing"]["name"], topic))
        time.sleep(10)


def basicPubSub(
    threadName,
    message,
    config,
    logLevel,
    customCallback):
    """basic pubsub method to be a thread
    """
    # init LOGGER
    if (logLevel == None):
        logLevel = logging.INFO
    logging.basicConfig(level=logLevel, format=LOG_FORMAT)

    # Init AWSIoTMQTTClient
    myAWSIoTMQTTClient = setupClient(
        config["thing"]["name"], 
        config["thing"]["endpoint"], 
        config["thing"]["port"], 
        "{0}/{1}".format(config["thing"]["keys"]["path"], config["thing"]["keys"]["rootCA"]), #rootca
        "{0}/{1}".format(config["thing"]["keys"]["path"], config["thing"]["keys"]["privateKey"]), #private key
        "{0}/{1}".format(config["thing"]["keys"]["path"], config["thing"]["keys"]["cert"]), #cert 
        config["thing"]["useWebsocket"])

    # Connect and subscribe to AWS IoT
    myAWSIoTMQTTClient.connect()
    LOGGER.info("connected to {0}".format(config["thing"]["endpoint"]))
    myAWSIoTMQTTClient.subscribe(config["thing"]["pubsub"]["topic"], 1, customCallback)
    time.sleep(2)

    # Publish to the same topic in a loop forever
    loopCount = 0
    loop = True
    while loop:
        try:
            messageModel = {}
            messageModel['message'] = message
            messageModel['sequence'] = loopCount
            messageJson = json.dumps(messageModel)
            myAWSIoTMQTTClient.publish(config["thing"]["pubsub"]["topic"], messageJson, 1)
            print('Published topic %s: %s\n' % (config["thing"]["pubsub"]["topic"], messageJson))
            loopCount += 1
            time.sleep(1)
        except:
            LOGGER.error("an error occured.")
            print("-"*60)
            traceback.print_exc(file=sys.stdout)
            print("-"*60)
            loop = False

def setupClient(
    clientId, host, port, 
    rootCAPath, privateKeyPath, 
    certificatePath, 
    useWebsocket):

    # Init AWSIoTMQTTClient
    myAWSIoTMQTTClient = None
    if useWebsocket:
        myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
        myAWSIoTMQTTClient.configureEndpoint(host, port)
        myAWSIoTMQTTClient.configureCredentials(rootCAPath)
    else:
        myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
        myAWSIoTMQTTClient.configureEndpoint(host, port)
        myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

    # AWSIoTMQTTClient connection configuration
    myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

    return myAWSIoTMQTTClient
