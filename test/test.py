 
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
import time # Librería para hacer que el programa que controla el bot no se acabe.
import random
import datetime

bot = telebot.TeleBot("207063163:AAH5GbFmvmNnNog6ZJ0QXI1ZI2KFX0rsxaI")

#Listener
def listener(messages): # Con esto, estamos definiendo una función llamada ‘listener’, que recibe como parámetro un dato llamado ‘messages’.
	for message in messages: # Por cada dato ‘m’ en el dato ‘messages’
		cid = message.chat.id # Almacenaremos el ID de la conversación.
		if message.content_type == 'text':
			print ('[' + str(cid) + ']: ' + message.text) 

bot.set_update_listener(listener) # Así, le decimos al bot que utilice como función escuchadora nuestra función ‘listener’ declarada arriba.

@bot.message_handler(commands=['start'])
def send_start(message):
    bot.send_message(message.chat.id, "Bienvenido a HomeBerry")

@bot.message_handler(commands=['help'])
def send_help(message):
    #bot.reply_to(message, "Esta es la lista de comandos que puedes usar: ...")
    bot.send_message(message.chat.id, "Esta es la lista de comandos que puedes usar: ...")

@bot.message_handler(commands=['logo'])
def send_logo(message):
    bot.send_photo( message.chat.id, open( 'raspberry.png', 'rb'))

@bot.message_handler(commands=['holamundo'])
def send_welcomeWorld(message):
    bot.send_message(message.chat.id, "Hola mundo!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, 'En desarrollo')

#############################################
#Peticiones
bot.polling(none_stop = True) # Con esto, le decimos al bot que siga funcionando incluso si encuentra algun fallo.























"""
import telebot
TOKEN = '207063163:AAH5GbFmvmNnNog6ZJ0QXI1ZI2KFX0rsxal' #Ponemos nuestro TOKEN generado con el @BotFather
bot = telebot.TeleBot(TOKEN) #Creamos nuestra instancia "mi_bot" a partir de ese TOKEN
####### COMMANDS #######

@bot.message_handler(commands=['start'])
def send_welcome(message):  
    cid = message.chat.id
    bot.send_message( cid, "Welcome to Sunrise & Sunset bot. With this bot you will be able to obtain sunset and sunrise times for a given location. Use the command /help to explore the different actions")


@bot.message_handler(commands=['help']) 
def command_help(m):  
    cid = m.chat.id 
    bot.send_message( cid, "These are the possible comands:\n/sunset: Obtain sunset time for a given location\n/sunrise: Obtain sunrise time for a given location\nday_length: Obtain the day length")

@bot.message_handler(commands=['sunrise']) 
def command_sunrise(m):  
    cid = m.chat.id 
    #To do

@bot.message_handler(commands=['sunset']) 
def command_sunset(m):  
    cid = m.chat.id 
    #To do

@bot.message_handler(commands=['day_length']) 
def command_daylength(m):  
    cid = m.chat.id 
    #To do  


##############     
bot.polling(none_stop=True)  
while True: #Infinite loop  
    pass
"""






#import pexpect
#import socket  # connect to telegram cli.
#import json
#import logging 

#telegram = pexpect.spawn('../../TelegramProject/tg/bin/telegram-cli -k tg-server.pub') #Inicia Telegram
#telegram.expect('0m')
#print telegram.after
#telegram.expect('\S*((\w\s\w)|(\w))+\S*$')
#print telegram.after  
#while (True):
#	print 'entre en el bucle'
#	telegram.expect('.+')
#	print telegram.after + telegram.before  
#contacto = "Julian_Avaca"                          #Contacto a quien va el mensaje
#mensaje = "Hola javi te escribo desde un programa de python, que usa de fondo el clinete-Telegram!!"              #Mensaje a enviar
#telegram.sendline('msg '+contacto+' '+mensaje)   #Ejecuta el comando msg
#print ('Mensaje enviado a '+ contacto)           #Notifica que ya se ha mandado el mensaje
#telegram.sendline('quit')                        #cierra Telegram