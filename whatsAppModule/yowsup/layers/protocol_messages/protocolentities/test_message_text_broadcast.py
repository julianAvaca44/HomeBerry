from whatsAppModule.yowsup.layers.protocol_messages.protocolentities.test_message_text import TextMessageProtocolEntityTest
from whatsAppModule.yowsup.layers.protocol_messages.protocolentities.message_text_broadcast import BroadcastTextMessage
from whatsAppModule.yowsup.structs import ProtocolTreeNode
class BroadcastTextMessageTest(TextMessageProtocolEntityTest):
    def setUp(self):
        super(BroadcastTextMessageTest, self).setUp()
        self.ProtocolEntity = BroadcastTextMessage
        broadcastNode = ProtocolTreeNode("broadcast")
        jids = ["jid1", "jid2"]
        toNodes = [ProtocolTreeNode("to", {"jid" : jid}) for jid in jids]
        broadcastNode.addChildren(toNodes)
        self.node.addChild(broadcastNode)
