#!/usr/bin/env python
import sys, argparse, logging
from whatsAppModule.yowsup.layers.interface                   import YowInterfaceLayer, ProtocolEntityCallback
from whatsAppModule.yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from whatsAppModule.yowsup.stacks import  YowStackBuilder
from whatsAppModule.yowsup.layers.auth import AuthError
from whatsAppModule.yowsup.layers import YowLayerEvent
from whatsAppModule.yowsup.layers.network import YowNetworkLayer
from whatsAppModule.yowsup.common.tools import Jid
import constantes as const
from analaizerModule import messageAnalizer as am
from actionModule import action as actm

from whatsAppModule.yowsup.layers.protocol_media.protocolentities import RequestUploadIqProtocolEntity
from whatsAppModule.yowsup.layers.protocol_media.mediauploader import MediaUploader
from whatsAppModule.yowsup.layers.protocol_media.protocolentities.message_media_downloadable_image import ImageDownloadableMediaMessageProtocolEntity

logger = logging.getLogger("yowsup-cli")

class WhatsAppBot(object):
    def __init__(self, encryptionEnabled = True):
        credentials = (const.TELEFONO, const.PASSWORD) 
        stackBuilder = YowStackBuilder()

        self.stack = stackBuilder\
            .pushDefaultLayers(encryptionEnabled)\
            .push(ListenerLayer)\
            .build()

        self.stack.setCredentials(credentials)

    def start(self):
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        try:
            self.stack.loop()
        except AuthError as e:
            print("Authentication Error: %s" % e.message)

    def _getCredentials(self):
        return const.TELEFONO, const.PASSWORD            

class ListenerLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        if messageProtocolEntity.getType() == 'text':
 	    	print("WA " + messageProtocolEntity.getFrom(False) + " : " + messageProtocolEntity.getBody())
                commands = am.analizarMessage(messageProtocolEntity.getBody())
                print(commands)
                message = actm.acction(commands)
                if(message == "photo"):
                    self.mediaSend(messageProtocolEntity.getFrom(False), './images/photo.jpg', RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE)
                else:
                    messageProtocolEntity.setBody(message)
                    self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))
                    self.toLower(messageProtocolEntity.ack())
        elif messageProtocolEntity.getType() == "media":
			if messageProtocolEntity.getMediaType() in ("audio"):
				fileOut = self.getDownloadableMediaMessageBody(messageProtocolEntity)
				messageText = am.convertSpeechToText(fileOut)
				commands = am.analizarMessage(messageText)
				message = actm.acction(commands)
				messageEntity = TextMessageProtocolEntity(message, to = self.normalizeJid(messageProtocolEntity.getFrom(False)))
				self.toLower(messageEntity)
				print 'Respuesta: %s' % message
			
        self.toLower(messageProtocolEntity.ack(True))
        
    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())

    def messageSend(self, number, content):
         outgoingMessage = TextMessageProtocolEntity(content.encode("utf-8") if sys.version_info >= (3,0) else content, to = self.aliasToJid(number))
         self.toLower(outgoingMessage)

    def mediaSend(self, number, path, mediaType, caption = None):
        jid = self.normalizeJid(number)
        entity = RequestUploadIqProtocolEntity(mediaType, filePath=path)                                            
        successFn = lambda successEntity, originalEntity: self.onRequestUploadResult(jid, mediaType, path, successEntity, originalEntity, caption)
        errorFn = lambda errorEntity, originalEntity: self.onRequestUploadError(jid, path, errorEntity, originalEntity)
        self._sendIq(entity, successFn, errorFn)

    def normalizeJid(self, number):
        if '@' in number:
            return number
        elif "-" in number:
            return "%s@g.us" % number

        return "%s@s.whatsapp.net" % number

    def onRequestUploadResult(self, jid, mediaType, filePath, resultRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity, caption = None):
        if resultRequestUploadIqProtocolEntity.isDuplicate():
            self.doSendMedia(mediaType, filePath, resultRequestUploadIqProtocolEntity.getUrl(), jid,
                             resultRequestUploadIqProtocolEntity.getIp(), caption)
            
        else:
            successFn = lambda filePath, jid, url: self.doSendMedia(mediaType, filePath, url, jid, resultRequestUploadIqProtocolEntity.getIp(), caption)
            mediaUploader = MediaUploader(jid, self.getOwnJid(), filePath,
                                      resultRequestUploadIqProtocolEntity.getUrl(),
                                      resultRequestUploadIqProtocolEntity.getResumeOffset(),
                                      successFn, None, None, async=False)
            mediaUploader.start()

        
    def doSendMedia(self, mediaType, filePath, url, to, ip = None, caption = None):
        if mediaType == RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE:
        	entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, ip, to, caption = caption)
        elif mediaType == RequestUploadIqProtocolEntity.MEDIA_TYPE_AUDIO:
        	entity = AudioDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, ip, to)
        elif mediaType == RequestUploadIqProtocolEntity.MEDIA_TYPE_VIDEO:
        	entity = VideoDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, ip, to, caption = caption)
        self.toLower(entity)


    def getDownloadableMediaMessageBody(self, message):
        filename = "./audio/voice%s"%message.getExtension() 
        with open(filename, 'wb') as f:
            f.write(message.getMediaContent())
        return filename
