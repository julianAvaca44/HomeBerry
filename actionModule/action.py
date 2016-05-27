#Obejtivo del action: recibe un comando y lo ejecuta
#es el encargado de comunicarse con las raspberry pi 3
#caso de algun fallo comunicar lo
# la idea de cuando llega un comando que analize un objecto con la siguiente estructura

listCommand = {
	'encender': func_1,
	'apagar': func_2,
	'activar': func_3,
	'desactivar': func_4,
}

#luego ejecutar la funcion, algo asi
#listCommand.[command]() revisar y buscar la manera lo estoy escribiendo a medida q se me ocurre pero la idea esta jajaj

import logging as log
#import RPi.GPIO as GPIO

log.basicConfig(filename='./action.log', filemode='w', level=log.DEBUG)

def acction(command):
	if command == None:
		return "comando no valido"	
	elif listCommand(command[0]) == 'encender':
		return "encender"

		#if command[0] in listCommand.keys(): 
		#	listCommand[command[0]]()
		#else:
		#	return "No se reconoce el commando" 
