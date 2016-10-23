from whatsAppModule.yowsup.stacks import  YowStackBuilder
from .layer import EchoLayer
from whatsAppModule.yowsup.layers.auth import AuthError
from whatsAppModule.yowsup.layers import YowLayerEvent
from whatsAppModule.yowsup.layers.network import YowNetworkLayer

class YowsupEchoStack(object):
    def __init__(self, credentials, encryptionEnabled = True):
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
