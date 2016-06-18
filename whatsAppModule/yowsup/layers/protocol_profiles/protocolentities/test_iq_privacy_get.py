from whatsAppModule.yowsup.layers.protocol_iq.protocolentities.test_iq import IqProtocolEntityTest
from whatsAppModule.yowsup.layers.protocol_profiles.protocolentities import GetPrivacyIqProtocolEntity
from whatsAppModule.yowsup.structs import ProtocolTreeNode

entity = GetPrivacyIqProtocolEntity()

class GetPrivacyIqProtocolEntityTest(IqProtocolEntityTest):
    def setUp(self):
        super(GetPrivacyIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = GetPrivacyIqProtocolEntity
        self.node = entity.toProtocolTreeNode()
