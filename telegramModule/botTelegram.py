#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
from telebot import types
import time # Librería para hacer que el programa que controla el bot no se acabe.
from analaizerModule import messageAnalizer as am
from actionModule import action
from securityModule import security as sec
import constantes as const
import wget
import os

#############################################
print "-- Module Telegram init --"
class BotTelegram():
	
		
	def __init__(self,db):
		self.db = db
		self.actm = action.action(db, self)

	def run(self):
		
		bot = telebot.TeleBot(const.TOKEN)
		self.actm.tele = bot
		#Listener
		def listener(messages): # Con esto, estamos definiendo una función llamada ‘listener’, que recibe como parámetro un dato llamado ‘messages’.
			for message in messages: # Por cada dato ‘m’ en el dato ‘messages’
				if message.content_type == 'contact':
					cid = message.chat.id # Almacenaremos el ID de la conversación.
					phone_number = int(message.contact.phone_number)
					user = self.db.users.find_one({'nro_telefono':phone_number})
					print (phone_number)
					print (user)
					if user == None:
						bot.send_message(cid, const.ERROR_USUARIO_NO_REGISTRADO)
					else:				
						markup = types.ReplyKeyboardHide()
						markup.hide_keyboard = True
						result = self.db.users.update_one({"_id":user['_id']}, {"$set":{'telegramId':cid}})						

						bot.send_message(cid, 'Telfono registrado', reply_markup=markup)

		bot.set_update_listener(listener) # Así, le decimos al bot que utilice como función escuchadora nuestra función ‘listener’ declarada arriba.


		@bot.message_handler(func = lambda message: True)
		def echo_all(message):
			cId = message.chat.id
			
			#Verifico que existe el usuario registrado 
			user = self.db.users.find_one({'telegramId':cId})
			if user != None:
				msg = message.text
				print (int(time.time()) - user['ultimaSolicitudCoordenadas'])
				msgCheckUserSession = sec.checkUserSession(user, msg, self.db)
				if(msgCheckUserSession != 'OK'):
					bot.send_message(cId, msgCheckUserSession)
				else:				
					if msg:
						#analizo, limpio y filtro los mensajes, parseo los msj a comandos
						print(str(cId) + " : " + message.chat.first_name + " : " + msg)
						commands = am.analizarMessage(msg)
						print("commads: ")
						print(commands)
						if(sec.checkUserProfileAcces(user, commands, self.db)):
							message = self.actm.acction(commands)
						else:
							message = "Tenés un perfil restringido para realizar esta acción"
						print message
						bot.send_message(cId, message)
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
				markup = types.ReplyKeyboardMarkup()
				markup.one_time_keyboard = True
				markup.resize_keyboard = True
				button = types.KeyboardButton('Enviar número de teléfono', request_contact=True)
				markup.add(button)
				bot.send_message(cId, 'Es necesario que nos envíes tu teléfono', reply_markup=markup)				
				print("Solicitar datos")				
			   
		@bot.message_handler(content_types=['voice', 'audio'])
		def echo_audio(message):   
			cId = message.chat.id
			fileAudio = bot.get_file(message.voice.file_id)
			urlFileAudio = "https://api.telegram.org/file/bot%s/%s" % (const.TOKEN,fileAudio.file_path)
			fileNameOutput = "./audio/voice.%s" % fileAudio.file_path[-3:]
			#Elimina archivo anterior - Esto debería modificarse para guardar mensajes anteriores
			try:
				os.remove(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "." + fileNameOutput)))
			except OSError:
				pass
			wget.download(urlFileAudio, fileNameOutput)
			messageText = am.convertSpeechToText(fileNameOutput)
			commands = am.analizarMessage(messageText)
			message = self.actm.acction(commands)
			bot.send_message(cId, message) 	

		
		def send_msg(self, cId, message, photo):
			bot.send_message(cId, message)
			if(photo != None):
				bot.send_photo(cId, open( './images/photo.jpg', 'rb'))			

		#Peticiones
		bot.polling(none_stop = True) # Con esto, le decimos al bot que siga funcionando incluso si encuentra algun fallo.



def telegramBotRun(db):
	bot = BotTelegram(db)
	bot.run()
	
	
