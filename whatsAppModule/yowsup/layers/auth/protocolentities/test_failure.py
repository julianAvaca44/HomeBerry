from whatsAppModule.yowsup.layers.auth.protocolentities.failure import FailureProtocolEntity
from whatsAppModule.yowsup.structs import ProtocolTreeNode
from whatsAppModule.yowsup.structs.protocolentity import ProtocolEntityTest
import unittest

class FailureProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = FailureProtocolEntity
        self.node = ProtocolTreeNode("failure", {}, [ProtocolTreeNode("not-authorized", {})])