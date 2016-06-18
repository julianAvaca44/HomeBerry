from .iq import IqProtocolEntity
from whatsAppModule.yowsup.structs import ProtocolTreeNode
class PropsIqProtocolEntity(IqProtocolEntity):
    def __init__(self):
        super(PropsIqProtocolEntity, self).__init__("w", _type="get")

    def toProtocolTreeNode(self):
        node = super(PropsIqProtocolEntity, self).toProtocolTreeNode()
        node.addChild(ProtocolTreeNode("props"))
        return node