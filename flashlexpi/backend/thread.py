import threading
import time, datetime
import json
import logging
import sys, traceback

from tinydb import TinyDB, Query
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')

LOGGER = logging.getLogger(__name__)

# init LOGGER
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

class ExpireMessagesThread(threading.Thread):
    def __init__(self, config):
        super(ExpireMessagesThread, self).__init__()
        self._expires = config["app"]["db"]["expireSeconds"]
        dbpath = "{0}/{1}".format(
            config["app"]["db"]["dataPath"], 
            config["app"]["db"]["subscriptionData"])
        self._db = TinyDB(dbpath)

    def run(self):
        print("running message cleanup")   
        if(self._expires>0):
            threshold = datetime.datetime.fromtimestamp(time.mktime(time.gmtime()))-datetime.timedelta(
                seconds=int(self._expires))
            ts = threshold.strftime("%s")    
            print(ts)    
            Messages = Query()
            self._db.remove(Messages.timestamp < float(ts))


class TopicSubscribeThread(threading.Thread):
    def __init__(self, config, customCallback):
        super(TopicSubscribeThread, self).__init__()
        self._config = config
        self.thingName = config["thing"]["name"]
        self._customCallback = customCallback
        self._iotClient = setupClientFromConfig(config)
        self.topic = config["thing"]["ingress"]["topic"]

    def run(self):
        """ save messages subscribed to to 
        local database
        """
        #topic="ingress/{0}".format(self.thingName)

        # Connect and subscribe to AWS IoT
        self._iotClient.connect()
        self._iotClient.subscribe(self.topic, 1, self._customCallback)
        time.sleep(2)    

        loop = True
        while loop:
            # LOGGER.debug("subscribe-{0} listening to topic: {1}".format(
            #     self.thingName, topic))
            time.sleep(10)

class BasicPubsubThread(threading.Thread):
    def __init__(self, message, config, customCallback):
        super(BasicPubsubThread, self).__init__()
        self.message = message
        self._config = config
        self.thingName = config["thing"]["name"]
        self._customCallback = customCallback
        self._iotClient = setupClientFromConfig(config)
        self.topic = config["thing"]["pubsub"]["topic"]

    def run(self):
        """ save messages subscribed to to 
        local database
        """
        # print("running")
        # topic="pubsub/{0}".format(self.thingName)

        # Connect and subscribe to AWS IoT
        self._iotClient.connect()
        self._iotClient.subscribe(self.topic, 1, self._customCallback)
        time.sleep(2)    

        # Publish to the same topic in a loop forever
        loopCount = 0
        loop = True
        while loop:
            try:
                messageModel = {}
                messageModel['message'] = self.message
                messageModel['sequence'] = loopCount
                messageJson = json.dumps(messageModel)
                self._iotClient.publish(self.topic, messageJson, 1)
                LOGGER.info('Published topic %s: %s\n' % (self.topic, messageJson))
                loopCount += 1
                time.sleep(1)
            except:
                LOGGER.error("an error occured.")
                print("-"*60)
                traceback.print_exc(file=sys.stdout)
                print("-"*60)
                loop = False

def setupClientFromConfig(config):
    return setupClient(
        config["thing"]["name"], 
        config["thing"]["endpoint"], 
        config["thing"]["port"], 
        "{0}/{1}".format(config["thing"]["keys"]["path"], config["thing"]["keys"]["rootCA"]), #rootca
        "{0}/{1}".format(config["thing"]["keys"]["path"], config["thing"]["keys"]["privateKey"]), #private key
        "{0}/{1}".format(config["thing"]["keys"]["path"], config["thing"]["keys"]["cert"]), #cert 
        config["thing"]["useWebsocket"])

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
