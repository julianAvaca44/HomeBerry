#!/usr/bin/env python
import sys, argparse, logging
from .yowsup.env import YowsupEnv
from whatsAppModule.yowsup.layers.interface                   import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.stacks import  YowStackBuilder
from yowsup.layers.auth import AuthError
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
import constantes as const
from analaizerModule import messageAnalizer as am
from actionModule import action as actm

logger = logging.getLogger("yowsup-cli")



class WhatsAppBot(object):
    def __init__(self, encryptionEnabled = True):
        credentials = (const.TELEFONO, const.PASSWORD) 
        stackBuilder = YowStackBuilder()

        self.stack = stackBuilder\
            .pushDefaultLayers(encryptionEnabled)\
            .push(EchoLayer)\
            .build()

        self.stack.setCredentials(credentials)

    def start(self):
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        try:
            self.stack.loop()
        except AuthError as e:
            print("Authentication Error: %s" % e.message)

    def _getCredentials(self):
        return const.TELEFONO, const.PASSWORD            

class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        if messageProtocolEntity.getType() == 'text':
 	    	print("WA " + messageProtocolEntity.getFrom(False) + " : " + messageProtocolEntity.getBody())
                commands = am.analizarMessage(messageProtocolEntity.getBody())
                print(commands)
                messageProtocolEntity.setBody(actm.acction(commands))

        self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))
        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))
        
    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())



         
