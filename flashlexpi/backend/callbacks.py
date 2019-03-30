import uuid
import time
import datetime
from tinydb import TinyDB, Query

class CallbackFactory:
    def get_callback_for_config(self, config):
        if config["app"]["callback"] == 'basicPubsub':
            return BasicPubsubCallbackHandler(config)
        elif config["app"]["callback"] == 'persistent':
            return PersistentCallbackHandler(config)            
        else:
            raise ValueError(config["app"]["callback"])

class BasicPubsubCallbackHandler(object):

    def __init__(self, config):
        self._client = config["thing"]["name"]
        self._type = "basicPubsub"

    def handleMessage(self, client, userdata, message):
        print("Received a new message on client:{0} type:{1}: ".format(self._client, self._type))
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")

    
class PersistentCallbackHandler(object):

    def __init__(self, config):
        self._client = config["thing"]["name"] 
        dbpath = "{0}/{1}".format(
            config["app"]["db"]["dataPath"], 
            config["app"]["db"]["subscriptionData"])
        self._db = TinyDB(dbpath)

        self._type = "persistent"

    def handleMessage(self, client, userdata, message):

        ts= time.time()
        messageDoc = {}
        messageDoc["pk"] = str(uuid.uuid4())
        messageDoc["timestamp"] = ts
        messageDoc["datetime"] = "{0}".format(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))        
        messageDoc["message"] = {
                "topic" : message.topic,
                "payload": str(message.payload),
                "pos": message.qos,
                "retain": message.retain,
                "mid": message.mid
        }

        self._db.insert(messageDoc)

        print("Received a new message on client:{0} type:{1}: ".format(self._client, self._type))
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")

factory = CallbackFactory()


