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


#PONER EN CONSTANTES O ALGUN LADO GENERAL O BASE DE DATOS
led = {}
led[1] = 4
led[2] = 17
ventilador = 18
tempHum = 23
movimiento = 24
sensorLuz = 25

#log.basicConfig(filename='./action.log', filemode='w', level=log.DEBUG)

waListener = None

class motionSensor (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        #La siguiente linea hace que cuando se cierre un thread se cierren todos
        self.daemon = True
        self.isRunning = False
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
		pir = MotionSensor(movimiento)
		while self.isRunning:
			time.sleep(1)
			if pir.motion_detected:
				funPhoto(None)
				print("Intruso detectado")
				if(waListener == None):
					print("No tiene listener de WA")
					try:
						waListener.sendMessage("Intruso detectado", True)	
					except:
						print("De verdad no tiene listener")
				else:
					waListener.sendMessage("Intruso detectado", True)
				time.sleep(600)

class lightSensor (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        #La siguiente linea hace que cuando se cierre un thread se cierren todos
        self.daemon = True
        self.isRunning = False
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
		while self.isRunning:
			time.sleep(2)
			if(GPIO.input(sensorLuz) != GPIO.input(led[1]) or  GPIO.input(sensorLuz) != GPIO.input(led[2])):
				messageToSend = ""
				if(GPIO.input(sensorLuz) == 1):
					funcOn(['encender', 'luces'])
					messageToSend = "Se encendieron las luces externas"
				else:
					funcOff(['encender', 'luces'])
					messageToSend = "Se apagaron las luces externas"
				print(messageToSend)
				if(waListener == None):
					print("No tiene listener de WA")
					try:
						waListener.sendMessage(messageToSend)	
					except:
						print("De verdad no tiene listener")
				else:
					waListener.sendMessage(messageToSend)
				time.sleep(1)

def acction(command,db):
	if command == None:
		return const.COMMAND_UNRECOGNIZABLE	
	elif command[0] in listCommand.keys(): 
		return listCommand[command[0]](command,db)
	else:
		return const.COMMAND_INVALID	

		
def funcOn(command,db):
	print "-- funcion On --"
	devices = db.devices.find({'tipo':command[1]})
	if(len(command) == 4):
		print command[1] + " - " + command[2] + " - " + command[3]
		device = db.devices.find_one({'tipo':command[1],'numero':int(command[2]),'idZona':command[3]})		
		#device = db.devices.find_one({'tipo':'luz','numero':1,'idZona':'Z1'})		
		print str(int(device['estado']))
		if(device == None):
			return const.DISP_INEXISTENTES
		elif((int(device['estado']) == 0) & (GPIO.input(device['pin']) == False)):
			GPIO.output(device['pin'], 1)
			db.devices.update_one({'tipo':command[1],'numero':int(command[2]),'idZona':command[3]},
				{'$set':{'estado':1}})
			return const.DISP_ON
		else:
			return device['tipo'] + " - " + str(device['numero']) + ": se encontraba encendida"	
	elif(len(command) == 3):
		if(command[1] == const.DISP_SENSOR):
			if(command[2] == const.DISP_LUZ):
				if objLightSensor.isRunning == False:
					objLightSensor.active()
					return "Sensor de luz activo"
				else:
					return "Sensor de luz se encontraba activado"
			else:
				return const.DISP_INEXISTENTES
		elif(command[1] == const.DISP_LUCES):
			lightsDevice = db.devices.find({'tipo':'Luz','idZona':command[3]})
			if(lightsDevice == None):
				return const.DISP_INEXISTENTES	
			#averiguo si todos los dispositivos ya estan encendidos
			lightsDeviceOff = db.devices.find({'tipo':'Luz','idZona':command[3],'estado':0})
			if (lightsDeviceOff == None):
				return "Los dispositivios ya se encontraban encendidos"
			#por el contrario enciendo el resto de dispositivos
			else:
				for deviceOff in lightsDeviceOff:
					if (int(deviceOff['estado']) == 0):
						GPIO.output(deviceOff['pin'], 1)	
				db.devices.update_many({'tipo':command[1],'idZona':command[3]},
					{'$set':{'estado':1}})
				return "dispositivios encendidos"
	elif(len(command) == 2):#comandos de dos terminos ej activar/encender alarma
		if(command[1] == const.DISP_ALARMA):
			if objMotionSensor.isRunning == False:
				objMotionSensor.active()
				return const.DISP_ACTIVADO_ALARMA
			else:
				return "Alarma se encontraba activada"
	else:
		return const.COMMAND_INVALID
	#logica para comunicarse con la rasp y prender el dispositivo deseado
	#comparar con el mapa de la casa
        	
	
def funcOff(command,db):
	print "-- funcion Off --"
	devices = db.devices.find({'tipo':command[1]})
	if(len(command) == 4):
		print command[1] + " - " + command[2] + " - " + command[3]
		device = db.devices.find_one({'tipo':command[1],'numero':int(command[2]),'idZona':command[3]})		
		#device = db.devices.find_one({'tipo':'luz','numero':1,'idZona':'Z1'})		
		print str(int(device['estado']))
		if(device == None):
			return const.DISP_INEXISTENTES
		elif(int(device['estado']) == 1 & GPIO.input(device['pin']) == True):
			GPIO.output(device['pin'], 0)
			db.devices.update_one({'tipo':command[1],'numero':int(command[2]),'idZona':command[3]},
				{'$set':{'estado':0}})
			return const.DISP_OFF
		else:
			return device['tipo'] + " - " + str(device['numero']) + ": se encontraba apagado"	
	elif(len(command) == 3):
		if(command[1] == const.DISP_SENSOR):
			if(command[2] == const.DISP_LUZ):
				if objLightSensor.isRunning == False:
					objLightSensor.active()
					return "Sensor de luz desactivado"
				else:
					return "Sensor de luz se encontraba desactivado"
			else:
				return const.DISP_INEXISTENTES
		elif(command[1] == const.DISP_LUCES):
			lightsDevice = db.devices.find({'tipo':'Luz','idZona':command[3]})
			if(lightsDevice == None):
				return const.DISP_INEXISTENTES	
			#averiguo si todos los dispositivos ya estan encendidos
			lightsDeviceOff = db.devices.find({'tipo':'Luz','idZona':command[3],'estado':0})
			if (lightsDeviceOff == None):
				return "Los dispositivios ya se encontraban apagados"
			#por el contrario enciendo el resto de dispositivos
			else:
				for deviceOff in lightsDeviceOff:
					if (int(deviceOff['estado']) == 1):
						GPIO.output(deviceOff['pin'], 0)	
				db.devices.update_many({'tipo':command[1],'idZona':command[3]},
					{'$set':{'estado':1}})
				return "dispositivios apagados"
	elif(len(command) == 2):#comandos de dos terminos ej activar/encender alarma
		if(command[1] == const.DISP_ALARMA):
			if objMotionSensor.isRunning == True:
				objMotionSensor.deactive()
				return const.DISP_DESACTIVADO_ALARMA
			else:
				return "Alarma se encontraba desactivada"
	else:
		return const.COMMAND_INVALID
	#logica para comunicarse con la rasp y prender el dispositivo deseado
	#comparar con el mapa de la casa

def funState(command,db):
	print("funState")
	#comando state: funcion que permite concer el estado de un dispositivo
	#tipo de comando de 3 columnas
	#ej: estado luz 1 ---> Luz 1 encendida
        if(command[1] == const.DISP_LUZ):
                if(command[2]== "1" or command[2]== "2"):
                        state = GPIO.input(led[int(command[2])])
                        return "Luz " + command[2] + " " + ("encendida" if state else "apagada")
                else:
                        return "Dispositivo inexistente"
        elif(command[1] == "luces"):
                state = GPIO.input(led[1])
                respuesta = "Luz 1 " + ("encendida" if state else "apagada")
                state = GPIO.input(led[2])        
                return respuesta + " - Luz 2 " + ("encendida" if state else "apagada")
        elif(command[1] == "ventilador"):
                state = GPIO.input(ventilador)
                return "Ventilador " + ("encendido" if state else "apagado")
        elif(command[1] == "dispositivos"):
                state = GPIO.input(led[1])
                respuesta = "Luz 1 " + ("encendida" if state else "apagada")
                state = GPIO.input(led[2])        
                respuesta = respuesta + "\nLuz 2 " + ("encendida" if state else "apagada")
                state = GPIO.input(ventilador)
                return respuesta + "\nVentilador " + ("encendido" if state else "apagado")
        elif(command[1] == "temperatura"):
                return "Temperatura: {0:0.1f} C".format(DHT.read_retry(22, tempHum)[1]) #0-humedad, 1-temperatura
        elif(command[1] == "humedad"):
                return "Humedad: {0:0.1f} %".format(DHT.read_retry(22, tempHum)[0]) #0-humedad, 1-temperatura
        else:
                return const.DISP_INEXISTENTES        

def funPhoto(command,db):
        os.system('fswebcam -q -r 320x240 -S 3 --no-banner --jpeg 50 --save ./images/photo.jpg') # uses Fswebcam to take picture
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


objMotionSensor = motionSensor()
objLightSensor = lightSensor()

