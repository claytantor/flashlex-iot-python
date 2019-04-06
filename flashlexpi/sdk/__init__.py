import yaml
import requests
import jwt
import uuid
import os,sys
import datetime

from tinydb import TinyDB, Query

def openFile(fileName):
    data = ""
    with open (fileName, "r") as f:
        data = f.read()
    return data

def createToken(thingId, payload, privateKey):
    return jwt.encode(payload, privateKey, algorithm='RS256', headers={'kid': thingId})
    
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
            self._config["flashlex"]["app"]["db"]["dataPath"], 
            self._config["flashlex"]["app"]["db"]["subscriptionData"])

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
        subscriptionDataPath = "{0}/{1}".format(
            self._config["flashlex"]["app"]["db"]["dataPath"], 
            self._config["flashlex"]["app"]["db"]["subscriptionData"])
        subscriptionDb = TinyDB(subscriptionDataPath)
        subscriptionDb.remove(doc_ids=[message.doc_id])
        subscriptionDb.close()
    
    def collectMessage(self, message):
        """
        uses the certificate to generate an asymetric token
        that can be verified by the public key at flashlex,
        messages cannot be collected unless the key is 
        verified.
        """
        thingId=self._config["flashlex"]["thing"]["id"]
        privateKey = openFile("{0}/{1}".format(
            self._config["flashlex"]["thing"]["keys"]["path"], 
            self._config["flashlex"]["thing"]["keys"]["privateKey"]))

        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=120),
            'nbf': datetime.datetime.utcnow(),
            'iss': 'urn:thing:{0}'.format(thingId),
            'aud': 'urn:flashlex:{0}'.format(thingId)
        }

        jwt = createToken(thingId, payload, privateKey)

        try:
            r = requests.post("{0}/things/{1}/collect".format(
                self._config["flashlex"]["app"]["endpoint"],
                self._config["flashlex"]["thing"]["id"]), 
                data = message, 
                headers={"Authorization":jwt})
            return r.status_code
        except:
            return 500
        


