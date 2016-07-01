#Obejtivo del action: recibe un comando y lo ejecuta
#es el encargado de comunicarse con las raspberry pi 3
#caso de algun fallo comunicar lo
# la idea de cuando llega un comando que analize un objecto con la siguiente estructura



#luego ejecutar la funcion, algo asi
#listCommand.[command]() revisar y buscar la manera lo estoy escribiendo a medida q se me ocurre pero la idea esta jajaj

import logging as log
import RPi.GPIO as GPIO
import os
import Adafruit_DHT as DHT
from gpiozero import MotionSensor
import threading
import time

#TODO: Mejorar esto!
#from whatsAppModule import whatsapp as wa


#PONER EN CONSTANTES O ALGUN LADO GENERAL
led = {}
led[1] = 4
led[2] = 17
ventilador = 18
tempHum = 23
movimiento = 24

log.basicConfig(filename='./action.log', filemode='w', level=log.DEBUG)

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
		print ("Alarma Activada")
    def deactive(self):
		self.isRunning = False
		print ("Alarma desactivada")		
    def checkMovements(self):
		pir = MotionSensor(movimiento)
		while self.isRunning:
			time.sleep(1)
			if pir.motion_detected:
				print("Intruso detectado")
				#TODO: Este grupo quedo duro, ver configuracion
				#whatsAppModule.messageSend("5491162737159-1467366059", "Intruso detectado")
				time.sleep(600)

def acction(command):
	if command == None:
		return "No se reconoce el commando"	
	elif command[0] in listCommand.keys(): 
		return listCommand[command[0]](command)
	else:
		return "Comando no valido" 

		
def funcOn(command):

	print("funcOn")
	if(command[1] == "luz"):
		if(len(command)>2 and ( command[2]== "1" or command[2]== "2")):
			if (GPIO.input(led[int(command[2])]) == False):
				GPIO.output(led[int(command[2])], 1)
				return "Luz " + command[2] + " encendida"
			else:
				return "Luz " + command[2] + " se encontraba encendida"
		else:
			return "Dispositivo inexistente"
	elif(command[1] == "luces"):
		if (GPIO.input(led[int(1)]) == False or GPIO.input(led[int(2)]) == False):
			GPIO.output(led[1], 1)
			GPIO.output(led[2], 1)
			return "Luces encendidas"                
		else:
			return "Luces se encontraban encendidas"
	elif(command[1] == "ventilador"):
		if (GPIO.input(ventilador) == False):
			GPIO.output(ventilador, 1)
			return "Ventilador encendido"
		else:
			return "Ventilador se encontraba encendido"
	elif(command[1] == "alarma"):
		if objMotionSensor.isRunning == False:
			objMotionSensor.active()
			return "Alarma activada"
		else:
			return "Alarma se encontraba activada"
	else:
		return "Dispositivo inexistente"
	#logica para comunicarse con la rasp y prender el dispositivo deseado
	#comparar con el mapa de la casa
        	
	
def funcOff(command):
	print("funcOff")
	#logica para comunicarse con la rasp y apgar el dispositivo deseado
	#comparar con el mapa de la casa
	if(command[1] == "luz"):
		if(len(command)>2 and (command[2]== "1" or command[2]== "2")):
			if (GPIO.input(led[int(command[2])])):
				GPIO.output(led[int(command[2])], 0)
				return "Luz " + command[2] +" apagada"
			else:
				return "Luz se encontraba apagada"
		else:
			return "Dispositivo inexistente"                
	elif(command[1] == "luces"):
		if (GPIO.input(led[int(1)]) == True or GPIO.input(led[int(2)]) == True):
			GPIO.output(led[1], 0)
			GPIO.output(led[2], 0)
			return "Luces apagadas"
		else:
			return "Luces se encontraban apagadas"

	elif(command[1] == "ventilador"):
		if (GPIO.input(ventilador)):
			GPIO.output(ventilador, 0)
			return "Ventilador apagado"
		else:
			return "Ventilador se encontraba apagado"
		
	elif(command[1] == "alarma"):
		if objMotionSensor.isRunning == True:
			objMotionSensor.deactive()
			return "Alarma desactivada"                
		else:
			return "Alarma se encontraba desactivada"                
	else:
		return "Dispositivo inexistente"

def funState(command):
	print("funState")
	#logica para comunicarse con la rasp y apgar el dispositivo deseado
	#comparar con el mapa de la casa
        if(command[1] == "luz"):
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
                return "Dispositivo inexistente"        

def funPhoto(command):
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

#wa.messageSend("5491162737159-1467366059", "prueba")
#print whatsAppModule.ListenerLayer.messageSend("5491162737159-1467366059", "prueba")


