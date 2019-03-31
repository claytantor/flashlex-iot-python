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


class ThreadTypeFactory:
    def get_thread_for_config(self, config, customCallback):
        if config["flashlex"]["app"]["thread"] == 'basicPubsub':
            return BasicPubsubThread(config, customCallback)
        elif config["flashlex"]["app"]["thread"] == 'subscribe':
            return TopicSubscribeThread(config, customCallback)            
        else:
            raise ValueError(config["flashlex"]["app"]["callback"])

class ExpireMessagesThread(threading.Thread):
    def __init__(self, config):
        super(ExpireMessagesThread, self).__init__()
        self._expires = config["flashlex"]["app"]["db"]["expireSeconds"]
        dbpath = "{0}/{1}".format(
            config["flashlex"]["app"]["db"]["dataPath"], 
            config["flashlex"]["app"]["db"]["subscriptionData"])
        self._db = TinyDB(dbpath)

    def run(self):
        LOGGER.info("running message cleanup")   
        if(self._expires>0):
            threshold = datetime.datetime.fromtimestamp(time.mktime(time.gmtime()))-datetime.timedelta(
                seconds=int(self._expires))
            ts = threshold.strftime("%s")      
            Messages = Query()
            self._db.remove(Messages.timestamp < float(ts))


class TopicSubscribeThread(threading.Thread):
    def __init__(self, config, customCallback):
        super(TopicSubscribeThread, self).__init__()
        self._config = config
        self.thingName = config["flashlex"]["thing"]["name"]
        self._customCallback = customCallback
        self._iotClient = setupClientFromConfig(config)
        self.topic = config["flashlex"]["thing"]["ingress"]["topic"]
        self._type = "subscribe"

    def getType(self):
        return self._type    

    def run(self):
        """ save messages subscribed to to 
        local database
        """
        #topic="ingress/{0}".format(self.thingName)

        # Connect and subscribe to AWS IoT
        self._iotClient.connect()
        self._iotClient.subscribe(self.topic, 1, self._customCallback)
        time.sleep(4)

        # try:
        #     messageModel = {}
        #     messageModel['message'] = "prime the pump"
        #     messageJson = json.dumps(messageModel)
        #     self._iotClient.publish(self.topic, messageJson, 1)
        #     LOGGER.info('Published topic %s: %s\n' % (self.topic, messageJson))
        #     loopCount += 1
        #     time.sleep(5)
        # except:
        #     LOGGER.error("an error occured.")
        #     print("-"*60)
        #     traceback.print_exc(file=sys.stdout)
        #     print("-"*60)
        #     loop = False    

        loop = True
        while loop:
            # LOGGER.info("subscribe-{0} listening to topic: {1}".format(
            #      self.thingName, self.topic))
            time.sleep(10)

class BasicPubsubThread(threading.Thread):
    def __init__(self, config, customCallback):
        super(BasicPubsubThread, self).__init__()    
        self._config = config
        self.message = config["flashlex"]["app"]["message"]
        self.thingName = config["flashlex"]["thing"]["name"]
        self._customCallback = customCallback
        self._iotClient = setupClientFromConfig(config)
        self.topic = config["flashlex"]["thing"]["pubsub"]["topic"]
        self._type = "basicPubsub"

    def getType(self):
        return self._type

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
                time.sleep(5)
            except:
                LOGGER.error("an error occured.")
                print("-"*60)
                traceback.print_exc(file=sys.stdout)
                print("-"*60)
                loop = False

def setupClientFromConfig(config):
    return setupClient(
        config["flashlex"]["thing"]["name"], 
        config["flashlex"]["thing"]["endpoint"], 
        config["flashlex"]["thing"]["port"], 
        "{0}/{1}".format(config["flashlex"]["thing"]["keys"]["path"], config["flashlex"]["thing"]["keys"]["rootCA"]), #rootca
        "{0}/{1}".format(config["flashlex"]["thing"]["keys"]["path"], config["flashlex"]["thing"]["keys"]["privateKey"]), #private key
        "{0}/{1}".format(config["flashlex"]["thing"]["keys"]["path"], config["flashlex"]["thing"]["keys"]["cert"]), #cert 
        config["flashlex"]["thing"]["useWebsocket"])

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

threadTypeFactory = ThreadTypeFactory()    
