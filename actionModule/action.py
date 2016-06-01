#Obejtivo del action: recibe un comando y lo ejecuta
#es el encargado de comunicarse con las raspberry pi 3
#caso de algun fallo comunicar lo
# la idea de cuando llega un comando que analize un objecto con la siguiente estructura



import logging as log
#import RPi.GPIO as GPIO

log.basicConfig(filename='./action.log', filemode='w', level=log.DEBUG)

def acction(command):
	if command == None:
		return "No se reconoce el commando"	
	elif command[0] in listCommand.keys(): 
		return listCommand[command[0]](command)
	else:
		return "Comando no valido" 

		
def funcOn(command):
	print "estoy en la funcion On"
	
	#logica para comunicarse con la rasp y prender el dispositivo deseado
	#comparar con el mapa de la casa
	return "dispositivio encendido"

def funcOff():
	print "estoy en la funcion 2"
	#logica para comunicarse con la rasp y apgar el dispositivo deseado
	#comparar con el mapa de la casa
	return "dispositivio apagado"

listCommand = {
	'encender': funcOn,
	'apagar': funcOff,
	'activar': funcOn,
	'desactivar': funcOff,
}

#luego ejecutar la funcion, algo asi
#listCommand.[command]() revisar y buscar la manera lo estoy escribiendo a medida q se me ocurre pero la idea esta jajaj
