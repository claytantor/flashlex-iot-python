import uuid
import time
import datetime
import json
from tinydb import TinyDB, Query

class CallbackFactory:
    def get_callback_for_config(self, config):
        if config["flashlex"]["app"]["callback"] == 'basicPubsub':
            return BasicPubsubCallbackHandler(config)
        elif config["flashlex"]["app"]["callback"] == 'persistent':
            return PersistentCallbackHandler(config)            
        else:
            raise ValueError(config["flashlex"]["app"]["callback"])

class BasicPubsubCallbackHandler(object):

    def __init__(self, config):
        self._client = config["flashlex"]["thing"]["name"]
        self._type = "basicPubsub"

    def handleMessage(self, client, userdata, message):
        print("Received a new message on client:{0} type:{1}: ".format(self._client, self._type))
        print(message.payload.decode("utf-8"))
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")

    
class PersistentCallbackHandler(object):

    def __init__(self, config):
        self._client = config["flashlex"]["thing"]["name"] 
        self._dbpath = "{0}/{1}".format(
            config["flashlex"]["app"]["db"]["dataPath"], 
            config["flashlex"]["app"]["db"]["subscriptionData"])
        # self._db = TinyDB(dbpath)

        self._type = "persistent"

    def handleMessage(self, client, userdata, message):

        ts= time.time()
        messageDoc = {}
        messageDoc["pk"] = str(uuid.uuid4()).replace("-","")[:12]
        messageDoc["timestamp"] = ts
        messageDoc["datetime"] = "{0}".format(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))        
        messageDoc["message"] = {
                "topic" : message.topic,
                "payload": json.loads(message.payload.decode("utf-8")),
                "pos": message.qos,
                "retain": message.retain,
                "mid": message.mid
        }
        
        db = TinyDB(self._dbpath)
        db.insert(messageDoc)
        db.close()

        print("Received a new message on client:{0} type:{1}: ".format(self._client, self._type))
        print(message.payload.decode("utf-8"))
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")

callbackFactory = CallbackFactory()


