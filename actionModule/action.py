#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Obejtivo del action: recibe un comando y lo ejecuta
#es el encargado de comunicarse con las raspberry pi 3
#caso de algun fallo comunicar lo
# la idea de cuando llega un comando que analize un objecto con la siguiente estructura

import logging as log
import RPi.GPIO as GPIO
import os
import Adafruit_DHT as DHT
from gpiozero import MotionSensor
import constantes as const
import threading
import time
import re
import urllib2


#log.basicConfig(filename='./action.log', filemode='w', level=log.DEBUG)


class action():

	tele = object
	
	def __init__(self, db, teleBot):
		self.db = db
		self.teleBot = teleBot
		
		#TODO: ver la posibilidad de varios sensores de cada tipo
		sensor = self.db.devices.find_one({'tipo':'sensormovimiento'})
		if (sensor != None):
			self.objMotionSensor = self.motionSensor(sensor['pin'], self.db, self)
		sensor = self.db.devices.find_one({'tipo':'sensorluz'})
		if (sensor != None):
			self.objLightSensor = self.lightSensor(sensor['_id'], self.db, self)
	
	class motionSensor (threading.Thread):
		def __init__(self, pin, db, actm):
			threading.Thread.__init__(self)
			#La siguiente linea hace que cuando se cierre un thread se cierren todos
			self.daemon = True
			self.isRunning = False
			self.db = db
			self.actm = actm
			self.pin = pin
			self.mutex = threading.Lock()
			self.mutex.acquire()
			self.start()
			
		def run(self):
			while True:
				self.mutex.acquire()
				self.checkMovements()
		def active(self):
			self.isRunning = True
			self.mutex.release()		
			print ("Alarma activada")
		def deactive(self):
			self.isRunning = False
			print ("Alarma desactivada")		
		def checkMovements(self):
			pir = MotionSensor(int(self.pin))
			while self.isRunning:
				time.sleep(1)
				if pir.motion_detected:
					self.actm.funPhoto(None, self.db)
					print("Intruso detectado")
					
					if(self.actm.teleBot != None):
						users = self.db.users.find({"perfil":"adulto"})
						for user in users:
							#self.actm.teleBot.send_msg(user['telegramId'], 'Intruso detectado', False)
							#TODO: Hacer de forma correcta este envío de mensajes!!!
							self.actm.tele.send_message(user['telegramId'], 'Intruso detectado')
							self.actm.tele.send_photo(user['telegramId'], open( './images/photo.jpg', 'rb'))
					
					'''
					if(waListener == None):
						print("No tiene listener de WA")
						try:
							waListener.sendMessage("Intruso detectado", True)	
						except:
							print("De verdad no tiene listener")
					else:
						waListener.sendMessage("Intruso detectado", True)
					'''
					time.sleep(600)
					


	class lightSensor (threading.Thread):
		def __init__(self, sensorId, db, actm):
			threading.Thread.__init__(self)
			#La siguiente linea hace que cuando se cierre un thread se cierren todos
			self.daemon = True
			self.isRunning = False
			self.db = db
			self.sensorId = sensorId
			self.actm = actm
			self.mutex = threading.Lock()
			self.mutex.acquire()
			self.start()
		def run(self):
			while True:
				self.mutex.acquire()
				self.checkLight()
		def active(self):
			self.isRunning = True
			self.mutex.release()		
			print ("Sensor de luz activado")
		def deactive(self):
			self.isRunning = False
			print ("Sensor de luz desactivado")
		def checkLight(self):
			sensor = self.db.devices.find_one({"_id":self.sensorId})
			while self.isRunning:
				time.sleep(2)
				devicesToActivate = self.db.devices.find({"accionadoSensor":self.sensorId})
				statusSensor = self.actm.checkStatus(sensor)
				print "Estado Sensor" + str(statusSensor)
				for device in devicesToActivate:
					statusDevice = self.actm.checkStatus(device)
					if(statusSensor != statusDevice and statusSensor == 1):
						self.actm.setOnDevice(device, self.db)
						print 'Encendiendo Luz'
					elif(statusSensor != statusDevice and statusSensor == 0):
						self.actm.setOffDevice(device, self.db)
						print 'Apagando Luz'
				time.sleep(1)
		
			
	def checkStatus(self, device):
		if(device['Wifi']):
			url = "http://" + device['nombreWifi']
			if(urllib2.urlopen(url).read()=="on"):
				return 1
			else:
				return 0
		else:
			return GPIO.input(int(device['pin']))

	def setOnDevice(self, device, db):
		if(device['Wifi']):
			url = "http://" + device['nombreWifi'] + "/MODULO=ON"
			urllib2.urlopen(url)
		else:
			GPIO.output(int(device['pin']), 1)
		db.devices.update({"_id":device["_id"]}, {'$set':{'estado':1}})

	def setOffDevice(self, device, db):
		if(device['Wifi']):
			url = "http://" + device['nombreWifi'] + "/MODULO=OFF"
			urllib2.urlopen(url)
		else:
			GPIO.output(int(device['pin']), 0)
		db.devices.update({"_id":device["_id"]}, {'$set':{'estado':0}})


	def acction(self, command):
		if command == None:
			return const.COMMAND_UNRECOGNIZABLE	
		elif command[0] in self.listCommand.keys(): 
			return self.listCommand[command[0]](self, command, self.db)
		else:
			return const.COMMAND_INVALID	

			
	def funcOn(self, command, db):
		print "-- funcion On --"
		if(command[1] == COMMAND_STATES):
			
		else:
			if(len(command) == 4):
				print command[1] + " - " + command[2] + " - " + command[3]
				device = db.devices.find_one({'tipo':command[1],'numero':int(command[2]),'idZona':command[3]})		
				if(device == None):
					return const.DISP_INEXISTENTES
				elif(self.checkStatus(device) == 0):
					self.setOnDevice(device, db)
					return const.DISP_ON
				else:
					return device['tipo'] + " - " + str(device['numero']) + ": se encontraba encendida"	
			elif(len(command) == 3):
				if(command[1] == const.DISP_SENSOR):
					if(command[2] == const.DISP_LUZ):
						if self.objLightSensor.isRunning == False:
							self.objLightSensor.active()
							return "Sensor de luz activo"
						else:
							return "Sensor de luz se encontraba activado"
					else:
						return const.DISP_INEXISTENTES	
				elif(command[1] == const.DISP_LUCES):
					lightsDevice = db.devices.find({'tipo':'luz','idZona':command[2]})
					if(lightsDevice == None):
						return const.DISP_INEXISTENTES	
					#averiguo si todos los dispositivos ya estan encendidos
					lightsDeviceOff = db.devices.find({'tipo':'luz','idZona':command[2],'estado':0})
					if (lightsDeviceOff == None):
						return "Los dispositivios ya se encontraban encendidos"
					#por el contrario enciendo el resto de dispositivos
					else:
						for deviceOff in lightsDeviceOff:
							self.setOnDevice(deviceOff, db)
							return "dispositivios encendidos"
				elif(command[1] == const.DISP_VENTILADOR):
					device = db.devices.find_one({'tipo':command[1],'idZona':command[2]})		
					if(device == None):
						return const.DISP_INEXISTENTES
					elif(self.checkStatus(device) == 0):
						self.setOnDevice(device, db)
						return "Ventildor encendido"
					else:
						return "El ventilador se encontraba encendido"
				
			elif(len(command) == 2):#comandos de dos terminos ej activar/encender alarma
				if(command[1] == const.DISP_ALARMA):
					if self.objMotionSensor.isRunning == False:
						self.objMotionSensor.active()
						return const.DISP_ACTIVADO_ALARMA
					else:
						return "Alarma se encontraba activada"
			else:
				return const.COMMAND_INVALID
			#logica para comunicarse con la rasp y prender el dispositivo deseado
			#comparar con el mapa de la casa
				
		
	def funcOff(self, command,db):
		print "-- funcion Off --"
		if(len(command) == 4):
			print command[1] + " - " + command[2] + " - " + command[3]
			device = db.devices.find_one({'tipo':command[1],'numero':int(command[2]),'idZona':command[3]})		
			if(device == None):
				return const.DISP_INEXISTENTES
			elif(self.checkStatus(device) == 1):
				self.setOffDevice(device, db)
				return const.DISP_OFF
			else:
				return device['tipo'] + " - " + str(device['numero']) + ": se encontraba apagado"	
		elif(len(command) == 3):
			if(command[1] == const.DISP_SENSOR):
				if(command[2] == const.DISP_LUZ):
					if self.objLightSensor.isRunning == False:
						self.objLightSensor.active()
						return "Sensor de luz desactivado"
					else:
						return "Sensor de luz se encontraba desactivado"
				else:
					return const.DISP_INEXISTENTES
			elif(command[1] == const.DISP_LUCES):
				lightsDevice = db.devices.find({'tipo':'luz','idZona':command[2]})
				if(lightsDevice == None):
					return const.DISP_INEXISTENTES	
				#averiguo si todos los dispositivos ya estan apagados
				lightsDeviceOn = db.devices.find({'tipo':'luz','idZona':command[2],'estado':1})
				if (lightsDeviceOn == None):
					return "Los dispositivios ya se encontraban apagados"
				#por el contrario enciendo el resto de dispositivos
				else:
					for deviceOn in lightsDeviceOn:
						self.setOffDevice(deviceOn, db)
					return "dispositivios apagados"					
			elif(command[1] == const.DISP_VENTILADOR):
				device = db.devices.find_one({'tipo':command[1],'idZona':command[2]})		
				#print str(int(device['estado']))
				if(device == None):
					print "Dispositivo no encontrado"
					return const.DISP_INEXISTENTES
					#(int(device['estado']) == 0) & --ESTO ESTABA EN EL IF
				elif(self.checkStatus(device) == 1):
					self.setOffDevice(device, db)
					return "Ventiladdor apagado"
				else:
					return "el Ventilador se encuentra apagado"	
		elif(len(command) == 2):#comandos de dos terminos ej activar/encender alarma
			if(command[1] == const.DISP_ALARMA):
				if self.objMotionSensor.isRunning == True:
					self.objMotionSensor.deactive()
					return const.DISP_DESACTIVADO_ALARMA
				else:
					return "Alarma se encontraba desactivada"
		else:
			return const.COMMAND_INVALID
		#logica para comunicarse con la rasp y prender el dispositivo deseado
		#comparar con el mapa de la casa

	def funState(self, command,db):
		print("funState")
		#comando state: funcion que permite concer el estado de un dispositivo
		#tipo de comando de 3 columnas
		#ej: estado luz 1 ---> Luz 1 encendida
		if(len(command) == 4):
			print command[1] + " - " + command[2] + " - " + command[3]
			device = db.devices.find_one({'tipo':command[1],'numero':int(command[2]),'idZona':command[3]})		
			if(device == None):
				return const.DISP_INEXISTENTES
			else:
				return device['tipo'] + command[2] + " de " + command[3] + " " + ("encendida" if self.checkStatus(device) else "apagada")
		elif(len(command) == 3):
			if(command[1] == const.DISP_SENSOR):
				if(command[2] == const.DISP_LUZ):
					return "Sensor de luz " + ("encendido" if self.objLightSensor.isRunning else "apagado")
				else:
					return const.DISP_INEXISTENTES
			elif(command[1] == const.DISP_LUCES):
				lightsDevice = db.devices.find({'tipo':'luz','idZona':command[2]})
				if(lightsDevice == None):
					return const.DISP_INEXISTENTES	
				else:
					respuesta = ""
					newLine = ""
					for device in lightsDevice:
							respuesta = respuesta + newLine + device['tipo'] + " " + str(device['numero']) + " de " + command[2] + " " +  ("encendida" if self.checkStatus(device) else "apagada")
							newLine = "\n"
					return respuesta
			elif(command[1] == const.DISP_VENTILADOR):
				device = db.devices.find_one({'tipo':'ventilador','idZona':command[2]})
				#print str(int(device['estado']))
				if(device == None):
					print "Dispositivo no encontrado"
					return const.DISP_INEXISTENTES
				else:
					return device['tipo'] + " de " + command[2] + " " + ("encendido" if self.checkStatus(device) else "apagado")

			elif(command[1] == const.DISP_HUMEDAD):
				device = db.devices.find_one({'tipo':'sensortemphum','idZona':command[2]})
				if(device == None):
					print "Dispositivo no configurado"
					return const.DISP_INEXISTENTES
				else:
					return "Humedad en " + command[2] + ":  {0:0.1f} %".format(DHT.read_retry(22, int(device['pin']))[0]) #0-humedad, 1-temperatura								
			elif(command[1] == const.DISP_TEMPERATURA):
				device = db.devices.find_one({'tipo':'sensortemphum','idZona':command[2]})
				if(device == None):
					print "Dispositivo no configurado"
					return const.DISP_INEXISTENTES
				else:
					return "Temperatura en " + command[2] + ":  {0:0.1f} C".format(DHT.read_retry(22, int(device['pin']))[1]) #0-humedad, 1-temperatura						
		elif(len(command) == 2):#comandos de dos terminos ej activar/encender alarma
			
			if(command[1] == const.DISP_ALARMA):
				if self.objMotionSensor.isRunning == True:
					return const.DISP_ACTIVADO_ALARMA
				else:
					return const.DISP_DESACTIVADO_ALARMA

			elif(command[1] == "dispositivos"):
				respuesta = ""
				newLine = ""
				devices = db.devices.find({'tipo':'luz'})
				for device in devices:
					respuesta = respuesta + newLine + device['tipo'] + " " + str(device['numero']) + " de " + device['idZona']  + " " + ("encendida" if self.checkStatus(device) else "apagada")
					newLine = "\n"
				
				devices = db.devices.find({'tipo':'ventilador'})
				for device in devices:
					respuesta = respuesta + newLine + device['tipo'] + " " + str(device['numero']) + " de " + device['idZona']  + " " +  ("encendido" if self.checkStatus(device) else "apagado")
					newLine = "\n"
				
				if self.objMotionSensor.isRunning == True:
					respuesta = respuesta + newLine + const.DISP_ACTIVADO_ALARMA
				else:
					respuesta = respuesta + newLine + const.DISP_DESACTIVADO_ALARMA
				
				if self.objLightSensor.isRunning == True:
					respuesta = respuesta + "\nSensor de luminosidad activado"
				else:
					respuesta = respuesta + "\nSensor de luminosidad desactivado"

				devices = db.devices.find({'tipo':'sensortemphum'})
				for device in devices:
					respuesta = respuesta + "\nTemperatura en " + device['idZona'] + ":  {0:0.1f} C".format(DHT.read_retry(22, int(device['pin']))[1]) #0-humedad, 1-temperatura
					respuesta = respuesta + "\nHumedad en " + device['idZona'] + ":  {0:0.1f} %".format(DHT.read_retry(22, int(device['pin']))[0]) #0-humedad, 1-temperatura
			
				return respuesta
				
		else:
			return const.DISP_INEXISTENTES
		
		return const.DISP_INEXISTENTES
		#logica para comunicarse con la rasp y prender el dispositivo deseado
		#comparar con el mapa de la casa


	def funPhoto(self, command,db):
			#os.system('fswebcam -q -r 320x240 -S 3 --no-banner --jpeg 50 --save ./images/photo.jpg') # uses Fswebcam to take picture
			os.system('LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libv4l/v4l1compat.so fswebcam -q -r 320x240 -S 3 --no-banner -F 10 --save test.jpeg')

			return "photo"
			



	listCommand = {
		'encender': funcOn,
		'apagar': funcOff,
		'activar': funcOn,
		'desactivar': funcOff,
		'estado': funState,
		'consultar': funState,	
		'foto': funPhoto
	}



