from whatsAppModule.yowsup.layers.protocol_iq.protocolentities.test_iq import IqProtocolEntityTest
from whatsAppModule.yowsup.layers.protocol_profiles.protocolentities import ResultPrivacyIqProtocolEntity
from whatsAppModule.yowsup.structs import ProtocolTreeNode

entity = ResultPrivacyIqProtocolEntity({"profile":"all","last":"none","status":"contacts"})

class ResultPrivacyIqProtocolEntityTest(IqProtocolEntityTest):
    def setUp(self):
        super(ResultPrivacyIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = ResultPrivacyIqProtocolEntity
        self.node = entity.toProtocolTreeNode()
