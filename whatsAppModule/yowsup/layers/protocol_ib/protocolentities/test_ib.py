from whatsAppModule.yowsup.layers.protocol_ib.protocolentities.ib import IbProtocolEntity
from whatsAppModule.yowsup.structs import ProtocolTreeNode
from whatsAppModule.yowsup.structs.protocolentity import ProtocolEntityTest
import unittest

class IbProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = IbProtocolEntity
        self.node = ProtocolTreeNode("ib")
