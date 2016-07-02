#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
import time # Librería para hacer que el programa que controla el bot no se acabe.
from analaizerModule import messageAnalizer as am
from actionModule import action as actm
#from HomeBerry.analaizerModule import messageAnalizer as am
import constantes as const

#############################################
print "-- Module Telegram init --"
class BotTelegram():
	def __init__(self,db):
		self.db = db

	def run(self):
		bot = telebot.TeleBot(const.TOKEN)
		
		@bot.message_handler(commands = ['start'])
		def send_start(message):
		    bot.send_message(message.chat.id, "Bienvenido a HomeBerry")

		@bot.message_handler(commands = ['help'])
		def send_help(message):
		    bot.send_message(message.chat.id, "Esta es la lista de comandos que puedes usar: /start /logo /holamundo /help")

		@bot.message_handler(commands = ['logo'])
		def send_logo(message):
		    bot.send_photo( message.chat.id, open( './images/raspberry.png', 'rb'))
	            #print("Archivo")

		@bot.message_handler(commands = ['holamundo'])
		def send_welcomeWorld(message):
		    bot.send_message(message.chat.id, "Hola mundo!")

		@bot.message_handler(func = lambda message: True)
		def echo_all(message):
		    #analizo, limpio y filtro los mensajes, parseo los msj a comandos
		    cId = message.chat.id
		    msg = message.text
		    if msg:
		    	print(str(cId) + " : " + message.chat.first_name + " : " + msg)
		    	commands = am.analizarMessage(msg)
		    	print("commads: ")
		    	print(commands)
		    else:
		    	pass
		    	#TODO:rechazar mensaje
		        #envio comando y reenvio respuesta al usuario
	            message = actm.acction(commands,self.db)
	            if(message == "photo"):
	                bot.send_photo(cId, open( './images/photo.jpg', 'rb'))
	            else:
	                bot.send_message(cId, message)
		#Peticiones
		bot.polling(none_stop = True) # Con esto, le decimos al bot que siga funcionando incluso si encuentra algun fallo.

def telegramBotRun(db):
	bot = BotTelegram(db)
	bot.run()