#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
import time # Librería para hacer que el programa que controla el bot no se acabe.
from analaizerModule import messageAnalizer as am
from actionModule import action as actm
import constantes as const
import wget
import os

#############################################

def telegramBotRun():
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
            message = actm.acction(commands)
            if(message == "photo"):
                bot.send_photo(cId, open( './images/photo.jpg', 'rb'))
            else:
                bot.send_message(cId, message)               
           
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
		message = actm.acction(commands)
		bot.send_message(cId, message) 		
		
	#Peticiones
	bot.polling(none_stop = True) # Con esto, le decimos al bot que siga funcionando incluso si encuentra algun fallo.
