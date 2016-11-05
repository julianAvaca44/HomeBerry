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
from actionModule import action as action
from securityModule import security as sec

from whatsAppModule.yowsup.layers.protocol_media.protocolentities import RequestUploadIqProtocolEntity
from whatsAppModule.yowsup.layers.protocol_media.mediauploader import MediaUploader
from whatsAppModule.yowsup.layers.protocol_media.protocolentities.message_media_downloadable_image import ImageDownloadableMediaMessageProtocolEntity

import threading

#logger = logging.getLogger("yowsup-cli")
		

class WhatsAppBot(object):
	def __init__(self, encryptionEnabled = True):
		credentials = (const.TELEFONO, const.PASSWORD) 
		stackBuilder = YowStackBuilder()
		self.stack = stackBuilder\
			.pushDefaultLayers(encryptionEnabled)\
			.push(ListenerLayer)\
			.build()

		self.stack.setCredentials(credentials)

	def start(self, db):
		objwhatsappListenerSender = whatsappListenerSender()
		#Ver este numero 8
		objListenerLayer = self.stack.getLayer(8)
		objwhatsappListenerSender.objwhatsappListenerLayer = objListenerLayer
		objAction = action.action(db, None)
		objAction.setWAListener(objwhatsappListenerSender)
		objListenerLayer.setAction(objAction)
		objListenerLayer.setDB(db)

		#actm.waListener = objwhatsappListenerSender
		self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
		
		while True:
			try:
				self.stack.loop()

			except AuthError as e:
				print("Authentication Error: %s" % e.message)
			#except:				
			#	print "ERROR"
			#	#pass

		  

	def _getCredentials(self):
		return const.TELEFONO, const.PASSWORD            

class ListenerLayer(YowInterfaceLayer):
	actm = None
	db = None

	def setAction(self, action):
		self.actm = action

	def setDB(self, db):
		self.db = db
	
	@ProtocolEntityCallback("message")
	def onMessage(self, messageProtocolEntity):
		#print("WA onMessage")
		#print 
		#print messageProtocolEntity.getFrom(True)
		user = sec.checkUser(messageProtocolEntity.getFrom(False), self.db)
	
		if user != None:
			msg = messageProtocolEntity.getBody()
			#print (int(time.time()) - user['ultimaSolicitudCoordenadas'])
			msgCheckUserSession = sec.checkUserSession(user, msg, self.db)
			if(msgCheckUserSession != 'OK'):
				messageProtocolEntity.setBody(msgCheckUserSession)
				self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))
				self.toLower(messageProtocolEntity.ack())
			else:				
				if msg:
					#analizo, limpio y filtro los mensajes, parseo los msj a comandos
					#print(str(cId) + " : " + message.chat.first_name + " : " + msg)
		
					if messageProtocolEntity.getType() == 'text':
						print("WA " + messageProtocolEntity.getFrom(False) + " : " + messageProtocolEntity.getBody())
						commands = am.analizarMessage(messageProtocolEntity.getBody())
						print(commands)
              
						'''
						elif messageProtocolEntity.getType() == "media":
							if messageProtocolEntity.getMediaType() in ("audio"):
								fileOut = self.getDownloadableMediaMessageBody(messageProtocolEntity)
								messageText = am.convertSpeechToText(fileOut)
								commands = am.analizarMessage(messageText)
								message = actm.acction(commands)
								messageEntity = TextMessageProtocolEntity(message, to = self.normalizeJid(messageProtocolEntity.getFrom(False)))
								self.toLower(messageEntity)
								print 'Respuesta: %s' % message					
						'''
						print("commads: ")
						if(sec.checkUserProfileAcces(user, commands, self.db)):
							message = self.actm.acction(commands)
							if(message == "photo"):
								self.mediaSend(messageProtocolEntity.getFrom(False), './images/photo.jpg', RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE)
							else:
								messageProtocolEntity.setBody(message)
								self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))
								self.toLower(messageProtocolEntity.ack()) 
						else:
							messageProtocolEntity.setBody(const.ERROR_USUARIO_RESTRINGIDO)
							self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))
							self.toLower(messageProtocolEntity.ack()) 						
						#print message
					else:
						print "NO ES TEXTO"
					
				else:
					pass
					#TODO:rechazar mensaje
					#envio comando y reenvio respuesta al usuario
					message = self.actm.acction(commands)
					if(message == "photo"):
						bot.send_photo(cId, open( './images/photo.jpg', 'rb'))
					else:
						bot.send_message(cId, message)   			
			
			
		

		else:
			messageProtocolEntity.setBody(const.ERROR_USUARIO_NO_REGISTRADO)
			self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))
			self.toLower(messageProtocolEntity.ack()) 

		
			
		self.toLower(messageProtocolEntity.ack(True))
		
	@ProtocolEntityCallback("receipt")
	def onReceipt(self, entity):
		self.toLower(entity.ack())

	def messageSend(self, number, content):
		outgoingMessage = TextMessageProtocolEntity(content.encode("utf-8") if sys.version_info >= (3,0) else content, to = self.normalizeJid(number))
		self.toLower(outgoingMessage)

	def mediaSend(self, number, path, mediaType = RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE, caption = None):
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

	def prueba(self):
		print "PRINT PRUEBA WA"

	def getDownloadableMediaMessageBody(self, message):
		filename = "./audio/voice%s"%message.getExtension() 
		with open(filename, 'wb') as f:
			f.write(message.getMediaContent())
		return filename
		
class whatsappListenerSender (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		#La siguiente linea hace que cuando se cierre un thread se cierren todos
		self.daemon = True
		self.mutex = threading.Lock()
		self.mutex.acquire()
		self.start()
		self.message = ""   
		self.user = "" 
		self.sendPhoto = False
		objwhatsappListenerLayer = None  

	def prueba(self, msg):
		self.objwhatsappListenerLayer.messageSend("5491162737159", msg) 
		
	def run(self):
		while True:
			self.mutex.acquire()
			if(self.objwhatsappListenerLayer != None):
				self.objwhatsappListenerLayer.messageSend(self.user, self.message)
				if(self.sendPhoto):
					self.objwhatsappListenerLayer.mediaSend(self.user, "./images/photo.jpg")
	
	def sendMessage(self, user, message, sendPhoto = False):
		self.mutex.release()		
		self.message = message
		self.user = user 
		self.sendPhoto = sendPhoto
