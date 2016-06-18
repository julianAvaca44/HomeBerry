from whatsAppModule.yowsup.stacks import YowStack
from .layer import SyncLayer
from whatsAppModule.yowsup.layers import YowLayerEvent
from whatsAppModule.yowsup.layers.auth                        import YowCryptLayer, YowAuthenticationProtocolLayer, AuthError
from whatsAppModule.yowsup.layers.coder                       import YowCoderLayer
from whatsAppModule.yowsup.layers.network                     import YowNetworkLayer
from whatsAppModule.yowsup.layers.stanzaregulator             import YowStanzaRegulator
from whatsAppModule.yowsup.layers.protocol_receipts           import YowReceiptProtocolLayer
from whatsAppModule.yowsup.layers.protocol_acks               import YowAckProtocolLayer
from whatsAppModule.yowsup.layers.logger                      import YowLoggerLayer
from whatsAppModule.yowsup.layers.protocol_contacts           import YowContactsIqProtocolLayer
from whatsAppModule.yowsup.layers                             import YowParallelLayer

class YowsupSyncStack(object):
    def __init__(self, credentials, contacts, encryptionEnabled = False):
        """
        :param credentials:
        :param contacts: list of [jid ]
        :param encryptionEnabled:
        :return:
        """
        if encryptionEnabled:
            from whatsAppModule.yowsup.layers.axolotl                     import YowAxolotlLayer
            layers = (
                SyncLayer,
                YowParallelLayer([YowAuthenticationProtocolLayer, YowContactsIqProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer]),
                YowAxolotlLayer,
                YowLoggerLayer,
                YowCoderLayer,
                YowCryptLayer,
                YowStanzaRegulator,
                YowNetworkLayer
            )
        else:
            layers = (
                SyncLayer,
                YowParallelLayer([YowAuthenticationProtocolLayer, YowContactsIqProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer]),
                YowLoggerLayer,
                YowCoderLayer,
                YowCryptLayer,
                YowStanzaRegulator,
                YowNetworkLayer
            )

        self.stack = YowStack(layers)
        self.stack.setProp(SyncLayer.PROP_CONTACTS, contacts)
        self.stack.setProp(YowAuthenticationProtocolLayer.PROP_PASSIVE, True)
        self.stack.setCredentials(credentials)

    def start(self):
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        try:
            self.stack.loop()
        except AuthError as e:
            print("Authentication Error: %s" % e.message)
