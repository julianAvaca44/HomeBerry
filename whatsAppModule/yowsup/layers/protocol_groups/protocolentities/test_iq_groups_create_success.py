from whatsAppModule.yowsup.structs.protocolentity import ProtocolEntityTest
from whatsAppModule.yowsup.layers.protocol_groups.protocolentities import SuccessCreateGroupsIqProtocolEntity
import unittest

entity = SuccessCreateGroupsIqProtocolEntity("123-456", "431-123")

class SuccessCreateGroupsIqProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = SuccessCreateGroupsIqProtocolEntity
        self.node = entity.toProtocolTreeNode()
