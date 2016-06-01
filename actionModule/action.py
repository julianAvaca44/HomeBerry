#Obejtivo del action: recibe un comando y lo ejecuta
#es el encargado de comunicarse con las raspberry pi 3
#caso de algun fallo comunicar lo
# la idea de cuando llega un comando que analize un objecto con la siguiente estructura



#luego ejecutar la funcion, algo asi
#listCommand.[command]() revisar y buscar la manera lo estoy escribiendo a medida q se me ocurre pero la idea esta jajaj

import logging as log
import RPi.GPIO as GPIO

#PONER EN CONSTANTES O ALGUN LADO GENERAL
led_1 = 4

log.basicConfig(filename='./action.log', filemode='w', level=log.DEBUG)

def acction(command):
	if command == None:
		return "No se reconoce el commando"	
	elif command[0] in listCommand.keys(): 
		return listCommand[command[0]](command)
	else:
		return "Comando no valido" 

		
def funcOn(command):
        print("estoy en la funcion 1")
        if(command[1] == "luz"):
                GPIO.output(led_1, 1)
                return "Luz encendida"
        elif(command[1] == "ventilador"):
                GPIO.output(led_1, 1)
                return "Ventilador encendido"
        else:
                return "Dispositivo inexistente"
	#logica para comunicarse con la rasp y prender el dispositivo deseado
	#comparar con el mapa de la casa
        	
	

def funcOff(command):
	print("estoy en la funcion 2")
	#logica para comunicarse con la rasp y apgar el dispositivo deseado
	#comparar con el mapa de la casa
        if(command[1] == "luz"):
                GPIO.output(led_1, 0)
                return "Luz apagada"
        elif(command[1] == "ventilador"):
                #GPIO.output(led_1, 0)
                return "Ventilador apagado"
        else:
                return "Dispositivo inexistente"


listCommand = {
	'encender': funcOn,
	'apagar': funcOff,
	'activar': funcOn,
	'desactivar': funcOff
}
