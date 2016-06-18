from .yowstack import YowStack, YowStackBuilder

from whatsAppModule.yowsup.layers.auth                        import YowCryptLayer, YowAuthenticationProtocolLayer, AuthError
from whatsAppModule.yowsup.layers.coder                       import YowCoderLayer
from whatsAppModule.yowsup.layers.logger                      import YowLoggerLayer
from whatsAppModule.yowsup.layers.network                     import YowNetworkLayer
from whatsAppModule.yowsup.layers.protocol_messages           import YowMessagesProtocolLayer
from whatsAppModule.yowsup.layers.stanzaregulator             import YowStanzaRegulator
from whatsAppModule.yowsup.layers.protocol_media              import YowMediaProtocolLayer
from whatsAppModule.yowsup.layers.protocol_acks               import YowAckProtocolLayer
from whatsAppModule.yowsup.layers.protocol_receipts           import YowReceiptProtocolLayer
from whatsAppModule.yowsup.layers.protocol_groups             import YowGroupsProtocolLayer
from whatsAppModule.yowsup.layers.protocol_presence           import YowPresenceProtocolLayer
from whatsAppModule.yowsup.layers.protocol_ib                 import YowIbProtocolLayer
from whatsAppModule.yowsup.layers.protocol_notifications      import YowNotificationsProtocolLayer
from whatsAppModule.yowsup.layers.protocol_iq                 import YowIqProtocolLayer
from whatsAppModule.yowsup.layers.protocol_contacts           import YowContactsIqProtocolLayer
from whatsAppModule.yowsup.layers.protocol_chatstate          import YowChatstateProtocolLayer
from whatsAppModule.yowsup.layers.protocol_privacy            import YowPrivacyProtocolLayer
from whatsAppModule.yowsup.layers.protocol_profiles           import YowProfilesProtocolLayer
from whatsAppModule.yowsup.layers.protocol_calls              import YowCallsProtocolLayer



YOWSUP_CORE_LAYERS = (
    YowLoggerLayer,
    YowCoderLayer,
    YowCryptLayer,
    YowStanzaRegulator,
    YowNetworkLayer
)


YOWSUP_PROTOCOL_LAYERS_BASIC = (
    YowAuthenticationProtocolLayer, YowMessagesProtocolLayer,
    YowReceiptProtocolLayer, YowAckProtocolLayer, YowPresenceProtocolLayer,
    YowIbProtocolLayer, YowIqProtocolLayer, YowNotificationsProtocolLayer,
    YowContactsIqProtocolLayer, YowChatstateProtocolLayer

)

YOWSUP_PROTOCOL_LAYERS_GROUPS = (YowGroupsProtocolLayer,) + YOWSUP_PROTOCOL_LAYERS_BASIC
YOWSUP_PROTOCOL_LAYERS_MEDIA  = (YowMediaProtocolLayer,) + YOWSUP_PROTOCOL_LAYERS_BASIC
YOWSUP_PROTOCOL_LAYERS_PROFILES  = (YowProfilesProtocolLayer,) + YOWSUP_PROTOCOL_LAYERS_BASIC
YOWSUP_PROTOCOL_LAYERS_CALLS  = (YowCallsProtocolLayer,) + YOWSUP_PROTOCOL_LAYERS_BASIC
YOWSUP_PROTOCOL_LAYERS_FULL = (YowGroupsProtocolLayer, YowMediaProtocolLayer, YowPrivacyProtocolLayer, YowProfilesProtocolLayer, YowCallsProtocolLayer)\
                              + YOWSUP_PROTOCOL_LAYERS_BASIC


YOWSUP_FULL_STACK = (YOWSUP_PROTOCOL_LAYERS_FULL,) +\
                     YOWSUP_CORE_LAYERS
