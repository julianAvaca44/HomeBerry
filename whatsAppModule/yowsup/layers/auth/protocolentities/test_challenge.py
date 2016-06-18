from whatsAppModule.yowsup.layers.auth.protocolentities.challenge import ChallengeProtocolEntity
from whatsAppModule.yowsup.structs import ProtocolTreeNode
from whatsAppModule.yowsup.structs.protocolentity import ProtocolEntityTest
import unittest

class ChallengeProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = ChallengeProtocolEntity
        attribs             = {}
        childNodes          = []
        data                = "dummydata"
        self.node = ProtocolTreeNode("challenge", attribs, [], data)