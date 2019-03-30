import yaml
from tinydb import TinyDB, Query

def loadConfig(configFile):
    cfg = None
    with open(configFile, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return cfg

def getSubscribedMessages(config):
    #client = config["thing"]["name"] 
    dbpath = "{0}/{1}".format(
            config["app"]["db"]["dataPath"], 
            config["app"]["db"]["subscriptionData"])
    db = TinyDB(dbpath)
    return db.all()
