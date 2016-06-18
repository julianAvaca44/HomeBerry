from whatsAppModule.yowsup.layers.protocol_notifications.protocolentities.notification_picture_set import SetPictureNotificationProtocolEntity
from whatsAppModule.yowsup.structs import ProtocolTreeNode
from whatsAppModule.yowsup.layers.protocol_notifications.protocolentities.test_notification_picture import PictureNotificationProtocolEntityTest

class SetPictureNotificationProtocolEntityTest(PictureNotificationProtocolEntityTest):
    def setUp(self):
        super(SetPictureNotificationProtocolEntityTest, self).setUp()
        self.ProtocolEntity = SetPictureNotificationProtocolEntity
        setNode = ProtocolTreeNode("set", {"jid": "SET_JID", "id": "123"}, None, None)
        self.node.addChild(setNode)
