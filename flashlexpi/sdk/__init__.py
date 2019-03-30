import yaml
from tinydb import TinyDB, Query

class FlashlexSDK(object):

    def __init__(self, configFile):
        self._config = self.loadConfig(configFile)
       
    def getConfig(self):
        return self._config
    
    def setConfig(self, config):
        self._config = config

       
    def loadConfig(self, configFile):
        cfg = None
        with open(configFile, 'r') as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        return cfg

    def getSubscribedMessages(self, count=-1, sortMessages=True, reverse=False):
        subscriptionDataPath = "{0}/{1}".format(
            self._config["app"]["db"]["dataPath"], 
            self._config["app"]["db"]["subscriptionData"])

        subscriptionDb = TinyDB(subscriptionDataPath)

        messages_all = subscriptionDb.all()
        subscriptionDb.close()

        if(sortMessages):
            sorted(messages_all, key=lambda message: message["timestamp"], reverse=reverse)
        if(count>0):
            return messages_all[:count]
        else:     
            return messages_all

    
    def removeMessageFromStore(self, message):
        #print("removing document with doc_id:{0}".format(message.doc_id))
        subscriptionDataPath = "{0}/{1}".format(
            self._config["app"]["db"]["dataPath"], 
            self._config["app"]["db"]["subscriptionData"])
        subscriptionDb = TinyDB(subscriptionDataPath)
        subscriptionDb.remove(doc_ids=[message.doc_id])
        subscriptionDb.close()


