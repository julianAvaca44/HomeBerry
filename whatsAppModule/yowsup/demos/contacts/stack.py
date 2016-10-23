from .layer import SyncLayer

from whatsAppModule.yowsup.stacks import  YowStackBuilder
from whatsAppModule.yowsup.layers.auth import AuthError
from whatsAppModule.yowsup.layers import YowLayerEvent
from whatsAppModule.yowsup.layers.auth import YowAuthenticationProtocolLayer
from whatsAppModule.yowsup.layers.network import YowNetworkLayer

class YowsupSyncStack(object):
    def __init__(self, credentials, contacts, encryptionEnabled = False):
        """
        :param credentials:
        :param contacts: list of [jid ]
        :param encryptionEnabled:
        :return:
        """
        stackBuilder = YowStackBuilder()

        self.stack = stackBuilder \
            .pushDefaultLayers(encryptionEnabled) \
            .push(SyncLayer) \
            .build()

        self.stack.setProp(SyncLayer.PROP_CONTACTS, contacts)
        self.stack.setProp(YowAuthenticationProtocolLayer.PROP_PASSIVE, True)
        self.stack.setCredentials(credentials)

    def start(self):
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        try:
            self.stack.loop()
        except AuthError as e:
            print("Authentication Error: %s" % e.message)
