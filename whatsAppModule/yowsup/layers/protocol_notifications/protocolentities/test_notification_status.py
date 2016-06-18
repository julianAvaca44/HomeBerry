from whatsAppModule.yowsup.layers.protocol_notifications.protocolentities.notification_status import StatusNotificationProtocolEntity
from whatsAppModule.yowsup.structs import ProtocolTreeNode
from whatsAppModule.yowsup.layers.protocol_notifications.protocolentities.test_notification import NotificationProtocolEntityTest

class StatusNotificationProtocolEntityTest(NotificationProtocolEntityTest):
    def setUp(self):
        super(StatusNotificationProtocolEntityTest, self).setUp()
        self.ProtocolEntity = StatusNotificationProtocolEntity
        setNode = ProtocolTreeNode("set", {}, [], "status_data")
        self.node.addChild(setNode)
