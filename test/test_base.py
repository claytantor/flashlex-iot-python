import unittest
import pathlib
import os, sys, traceback
import yaml

from os.path import dirname, abspath
from shutil import copyfile
from flashlexiot.backend.thread import BasicPubsubThread, ExpireMessagesThread
from flashlexiot.sdk import FlashlexSDK

def loadConfig(configFile):
    cfg = None
    with open(configFile, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    return cfg

class TestFlashlexSDK(unittest.TestCase):

    def setUp(self):
        fn = pathlib.Path(__file__).parent / 'test-config.yml'

         #get defaults for data and keys
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config = loadConfig("{0}/test-config.yml".format(dir_path))

        self.sdk = FlashlexSDK(config)

        config = self.sdk.getConfig()
        config["flashlex"]["app"]["db"]["dataPath"] = pathlib.Path(__file__).parent 
        config["flashlex"]["app"]["db"]["subscriptionData"] = 'data/subscription1.json'
        self.sdk.setConfig(config)

        #create a copy of the db with messages so one can be removed and tested
        src = pathlib.Path(__file__).parent / 'data/subscription1.json'
        dest = pathlib.Path(__file__).parent / 'data/subscription1_copy.json'
        copyfile(src, dest)

    def test_load_config(self):
        self.assertEqual('testThing1', self.sdk.getConfig()["flashlex"]["thing"]["name"])

    def test_get_messages(self):
        messages = self.sdk.getSubscribedMessages()
        self.assertEqual(7,len(messages))

    def test_remove_message(self):
        config = self.sdk.getConfig()
        config["flashlex"]["app"]["db"]["dataPath"] = pathlib.Path(__file__).parent 
        config["flashlex"]["app"]["db"]["subscriptionData"] = 'data/subscription1_copy.json'
        self.sdk.setConfig(config)
        messages = self.sdk.getSubscribedMessages()
        self.sdk.removeMessageFromStore(messages[0])
        messages = self.sdk.getSubscribedMessages()
        self.assertEqual(6,len(messages))



if __name__ == '__main__':
    unittest.main()
