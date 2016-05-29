#Obejtivo del action: recibe un comando y lo ejecuta
#es el encargado de comunicarse con las raspberry pi 3
#caso de algun fallo comunicar lo
# la idea de cuando llega un comando que analize un objecto con la siguiente estructura



#luego ejecutar la funcion, algo asi
#listCommand.[command]() revisar y buscar la manera lo estoy escribiendo a medida q se me ocurre pero la idea esta jajaj

import logging as log
import RPi.GPIO as GPIO

#PONER EN CONSTANTES O ALGUN LADO GENERAL
led = 4

log.basicConfig(filename='./action.log', filemode='w', level=log.DEBUG)

def acction(command):
	if command == None:
		return "No se reconoce el commando"	
	elif command[0] in listCommand.keys(): 
		return listCommand[command[0]]()
	else:
		return "Comando no valido" 

		
def funcOn():
	print("estoy en la funcion 1")
	#logica para comunicarse con la rasp y prender el dispositivo deseado
	#comparar con el mapa de la casa
        GPIO.output(led, 1)	
	return "dispositivo encendido"

def funcOff():
	print("estoy en la funcion 2")
	#logica para comunicarse con la rasp y apgar el dispositivo deseado
	#comparar con el mapa de la casa
	GPIO.output(led, 0)
	return "dispositivo apagado"


listCommand = {
	'encender': funcOn,
	'apagar': funcOff,
	'activar': funcOn,
	'desactivar': funcOff
}
