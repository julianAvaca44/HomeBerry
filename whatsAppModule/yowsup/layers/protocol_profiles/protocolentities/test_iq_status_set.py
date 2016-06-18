from whatsAppModule.yowsup.layers.protocol_iq.protocolentities.test_iq import IqProtocolEntityTest
from whatsAppModule.yowsup.layers.protocol_profiles.protocolentities import SetStatusIqProtocolEntity
from whatsAppModule.yowsup.structs import ProtocolTreeNode

class SetStatusIqProtocolEntityTest(IqProtocolEntityTest):
    def setUp(self):
        super(SetStatusIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = SetStatusIqProtocolEntity
        statusNode = ProtocolTreeNode("status", {}, [], "Hey there, I'm using WhatsApp")
        self.node.addChild(statusNode)
