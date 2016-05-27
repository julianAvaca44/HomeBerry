#Obejtivo del action: recibe un comando y lo ejecuta
#es el encargado de comunicarse con las raspberry pi 3
#caso de algun fallo comunicar lo
# la idea de cuando llega un comando que analize un objecto con la siguiente estructura
"""
listCommand = {
	'nameFunc_1': func_1,
	'nameFunc_2': func_2,
	'nameFunc_3': func_3,
	'nameFunc_4': func_4,
}

"""
#luego ejecutar la funcion, algo asi
#listCommand.[command]() revisar y buscar la manera lo estoy escribiendo a medida q se me ocurre pero la idea esta jajaj

import logging as log
#import RPi.GPIO as GPIO

log.basicConfig(filename='./action.log', filemode='w', level=log.DEBUG)

def acction(command):
	if command == None:
		return "comando no valido"	
	elif command[0] == 'encender':
		return "encender"
