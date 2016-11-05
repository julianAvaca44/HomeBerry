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
from time import sleep
import re
import urllib2


#log.basicConfig(filename='./action.log', filemode='w', level=log.DEBUG)


class action():

	tele = object
	waListener = None
    
	def setWAListener(self, waListener):
		self.waListener = waListener
	
	def __init__(self, db, teleBot):
		self.db = db
		self.teleBot = teleBot
		
		self.objSenderMessage = self.senderMessage(self.db, self)
		
		#TODO: ver la posibilidad de varios sensores de cada tipo
		sensor = self.db.devices.find_one({'tipo':'sensormovimiento'})
		if (sensor != None):
			self.objMotionSensor = self.motionSensor(sensor['pin'], self.db, self, self.objSenderMessage)
		sensor = self.db.devices.find_one({'tipo':'sensorluz'})
		if (sensor != None):
			self.objLightSensor = self.lightSensor(sensor['_id'], self.db, self)
		
	
	
	class motionSensor (threading.Thread):
		def __init__(self, pin, db, actm, objSenderMessage):
			threading.Thread.__init__(self)
			#La siguiente linea hace que cuando se cierre un thread se cierren todos
			self.daemon = True
			self.isRunning = False
			self.db = db
			self.actm = actm
			self.pin = pin
			self.objSenderMessage = objSenderMessage
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
			buzzer = self.db.devices.find_one({"tipo":"buzzer"})
			doorSensor = self.db.devices.find_one({"tipo":"sensorpuerta"})
			pir = MotionSensor(int(self.pin))
			while self.isRunning:
				time.sleep(1)
				statusDoorSensor = False
				print time.time()
				if(doorSensor != None):
					statusDoorSensor = self.actm.checkStatus(doorSensor)
					print statusDoorSensor
					#print "statusDoorSensor" + str(statusDoorSensor)
				
				if pir.motion_detected or statusDoorSensor:
					self.actm.funPhoto(None, self.db)
					print("Intruso detectado")
					#if(self.actm.teleBot != None):
					self.objSenderMessage.prepareMessage("Intruso detectado", None, "adulto")
					self.objSenderMessage.prepareMessage("photo", None, "adulto")

					'''
					for user in users:
						if(self.actm.waListener == None):
							print("No tiene listener de WA")
							try:
								self.actm.waListener.sendMessage(user[const.MONOGO_TELEFONO], "Intruso detectado", True)	
							except:
								print("De verdad no tiene listener")
						else:
							self.actm.waListener.sendMessage(user[const.MONOGO_TELEFONO],"Intruso detectado", True)
					'''
					
					timerBuzzer = 0
					while self.isRunning and timerBuzzer < 300:
						if(buzzer != None):
							self.actm.setOnDevice(buzzer, self.db)
							time.sleep(0.5)
							self.actm.setOffDevice(buzzer, self.db)
							time.sleep(0.5)
							timerBuzzer = timerBuzzer + 2
							
					#time.sleep(600)
					


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

		
	class senderMessage (threading.Thread):
		def __init__(self, db, actm):
			threading.Thread.__init__(self)
			#La siguiente linea hace que cuando se cierre un thread se cierren todos
			self.messageToSend = []
			self.number = []
			self.daemon = True
			self.db = db
			self.actm = actm
			self.mutex = threading.Lock()
			self.mutex.acquire()

			self.start()

		def run(self):
			while True:
				print "A-Sender"
				self.mutex.acquire()
				while len(self.messageToSend) > 0:
					while len(self.number[0]):
						self.sendMessage(self.messageToSend[0],self.number[0][0])
						self.number[0].pop(0)
					self.number.pop(0)
					self.messageToSend.pop(0)
		
		def prepareMessage(self, message, number=None, perfil=None):
			if(perfil != None):
				users = self.db.users.find({"perfil":perfil})
			else:
				users = self.db.users.find({"telefono":number})

			self.messageToSend.append(message)
			usersToSend = []
			for user in users:
				usersToSend.append(user['telegramId'])
			self.number.append(usersToSend)
			
			try:
				self.mutex.release()
			except:
				pass
		
		def sendMessage(self, message, phone):
			print "sender sendMessage"
			if(self.actm.teleBot != None):			
				if(message != "photo"):
					self.actm.tele.send_message(phone, message)
				else:
					self.actm.tele.send_photo(phone, open( './images/photo.jpg', 'rb'))			
							

			
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
		print 'setOn ' + device['_id'] + ' ' + device['nombre']
		if(device['Wifi']):
			url = "http://" + device['nombreWifi'] + "/MODULO=ON"
			urllib2.urlopen(url)
		else:
			GPIO.output(int(device['pin']), 1)
		db.devices.update({"_id":device["_id"]}, {'$set':{'estado':1}})

	def setOffDevice(self, device, db):
		print 'setOff ' + device['_id'] + ' ' + device['nombre']
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

	def checkIsAState(command, db):
		checkState = ""
		for msg in command:
			checkState = chechState +  ' ' + msg
		checkState = checkState[1:]
		print "es estadodo?-" +checkState + "-"
		state = db.states.find_one({"nombre":checkState})
		return (state != None)


			
	def funcOn(self, command, db):
		print "-- funcion On --"
		try:
			if(command[1] == const.COMMAND_STATES):
				stateMsg = command[2]
				i = 3
				while i < len(command):
					stateMsg = stateMsg + " " + command[i]
					i = i +1
				print "estado: " + stateMsg
				state = db.states.find_one({"nombre":stateMsg})
				if(state != None):
					print state
					for deviceState in state['dispositivos']:
						print  deviceState
						if(deviceState['id'] == const.DISP_ALARMA):
							if (deviceState['estado'] == 0 and self.objMotionSensor.isRunning == True):
								self.objMotionSensor.deactive()
								print "alarma desactivada"
							elif (deviceState['estado'] == 1 and self.objMotionSensor.isRunning == False):
								self.objMotionSensor.active()
								print "alarma activada"
						else:
							device = self.db.devices.find_one({"_id":deviceState['id']})
							if(device != None):
								if(deviceState['estado'] == 1):
									self.setOnDevice(device, db)
								else:
									self.setOffDevice(device, db)
					return "Estado iniciado"
				else:
					return "Estado inexistente"
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
							return "Los dispositivos ya se encontraban encendidos"
						#por el contrario enciendo el resto de dispositivos
						else:
							for deviceOff in lightsDeviceOff:
								self.setOnDevice(deviceOff, db)
								return "dispositivos encendidos"
					elif(command[1] == const.DISP_VENTILADOR):
						device = db.devices.find_one({'tipo':command[1],'idZona':command[2]})		
						if(device == None):
							return const.DISP_INEXISTENTES
						elif(self.checkStatus(device) == 0):
							self.setOnDevice(device, db)
							return "Ventilador encendido"
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
		except ValueError as e:
			pass
			return const.COMMAND_INVALID
		
		except:
			return const.COMMAND_INVALID
			pass
				
		
	def funcOff(self, command,db):
		print "-- funcion Off --"
		try:
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
						if self.objLightSensor.isRunning == True:
							self.objLightSensor.deactive()
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
						return "Los dispositivos ya se encontraban apagados"
					#por el contrario enciendo el resto de dispositivos
					else:
						for deviceOn in lightsDeviceOn:
							self.setOffDevice(deviceOn, db)
						return "dispositivos apagados"					
				elif(command[1] == const.DISP_VENTILADOR):
					device = db.devices.find_one({'tipo':command[1],'idZona':command[2]})		
					#print str(int(device['estado']))
					if(device == None):
						print "Dispositivo no encontrado"
						return const.DISP_INEXISTENTES
						#(int(device['estado']) == 0) & --ESTO ESTABA EN EL IF
					elif(self.checkStatus(device) == 1):
						self.setOffDevice(device, db)
						return "Ventilador apagado"
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
		except ValueError as e:
			pass
			return const.COMMAND_INVALID
		
		except:
			pass
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
				device = db.devices.find_one({'tipo':const.DISP_VENTILADOR,'idZona':command[2]})
				#print str(int(device['estado']))
				if(device == None):
					print "Dispositivo no encontrado"
					return const.DISP_INEXISTENTES
				else:
					return device['tipo'] + " de " + command[2] + " " + ("encendido" if self.checkStatus(device) else "apagado")

			elif(command[1] == const.DISP_HUMEDAD):
				print "sensor humedad"
				device = db.devices.find_one({'tipo':'sensortemphum','idZona':command[2]})
				if(device == None):
					print "Dispositivo no configurado"
					return const.DISP_INEXISTENTES
				else:
					if(DHT.read_retry(22, int(device['pin']))[0] != None):
						return "Humedad en " + command[2] + ":  {0:0.1f} %".format(DHT.read_retry(22, int(device['pin']))[0]) #0-humedad, 1-temperatura								
					else:
						return "Problemas con el dispositivo de humedad, por favor verifique el mismo"
			elif(command[1] == const.DISP_TEMPERATURA):
				print "sensor temperatura"
				device = db.devices.find_one({'tipo':'sensortemphum','idZona':command[2]})
				if(device == None):
					print "TEMP INEX"
					print "Dispositivo no configurado"
					return const.DISP_INEXISTENTES
				else:
					print "TEMP"
					if(DHT.read_retry(22, int(device['pin']))[1] != None):
						return "Temperatura en " + command[2] + ":  {0:0.1f} C".format(DHT.read_retry(22, int(device['pin']))[1]) #0-humedad, 1-temperatura						
					else:
						return "Problemas con el dispositivo de temperatura, por favor verifique el mismo"
					
					
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
				
				devices = db.devices.find({'tipo':const.DISP_VENTILADOR})
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
					if(DHT.read_retry(22, int(device['pin']))[1] != None):
						respuesta = respuesta + "\nTemperatura en " + device['idZona'] + ":  {0:0.1f} C".format(DHT.read_retry(22, int(device['pin']))[1]) #0-humedad, 1-temperatura
						respuesta = respuesta + "\nHumedad en " + device['idZona'] + ":  {0:0.1f} %".format(DHT.read_retry(22, int(device['pin']))[0]) #0-humedad, 1-temperatura
			
				return respuesta
				
		else:
			return const.DISP_INEXISTENTES
		
		return const.DISP_INEXISTENTES
		#logica para comunicarse con la rasp y prender el dispositivo deseado
		#comparar con el mapa de la casa


	def funPhoto(self, command, db):
			#os.system('fswebcam -q -r 320x240 -S 3 --no-banner --jpeg 50 --save ./images/photo.jpg') # uses Fswebcam to take picture
			os.system('LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libv4l/v4l1compat.so fswebcam -q -r 320x240 --rotate 90 -S 3 --no-banner -F 10 --save ./images/photo.jpg')
			return "photo"
		
	def funOpen(self, command,db):
		#check command 2 si existe en mongo
		#traer device de commando 2
		#y setear sus pines con lo valores correspondientes
		if command[1] == 'porton':
			if GPIO.input(13) == 0:
				return 'El porton esta abierto'
			else:
				print "Going forwards"
				GPIO.output(13,0)
				GPIO.output(19,1)
				GPIO.output(26,1)
		 
				sleep(1.4)
				print "Now stop"
				#los fines de carrera que funciona como el pulsador deben ejecutr esta linea
				GPIO.output(26,GPIO.LOW)
				return "Porton abierto..."
			
	def funClose(self, command,db):
		if command[1] == 'porton':
			if GPIO.input(13) == 1:
				return 'El porton esta cerrado'
			else:
				print "Going backwards"
				print GPIO.input(13)
				GPIO.output(13,1)
				GPIO.output(19,0)
				GPIO.output(26,1)
		 
				sleep(1.5)
				print "Now stop"
				GPIO.output(26,GPIO.LOW)
				return "Porton Cerrado..."
			

	listCommand = {
		'prender': funcOn,
		'encender': funcOn,
		'apagar': funcOff,
		'activar': funcOn,
		'desactivar': funcOff,
		'estado': funState,
		'consultar': funState,	
		'foto': funPhoto,
		'abrir':funOpen,
		'cerrar':funClose
	}



