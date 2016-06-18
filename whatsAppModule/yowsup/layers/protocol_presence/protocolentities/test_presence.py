from whatsAppModule.yowsup.layers.protocol_presence.protocolentities.presence import PresenceProtocolEntity
from whatsAppModule.yowsup.structs import ProtocolTreeNode
from whatsAppModule.yowsup.structs.protocolentity import ProtocolEntityTest
import unittest

class PresenceProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = PresenceProtocolEntity
        self.node = ProtocolTreeNode("presence", {"type": "presence_type", "name": "presence_name"}, None, None)
