#Obejtivo del action: recibe un comando y lo ejecuta
#es el encargado de comunicarse con las raspberry pi 3
#caso de algun fallo comunicar lo
# la idea de cuando llega un comando que analize un objecto con la siguiente estructura



#luego ejecutar la funcion, algo asi
#listCommand.[command]() revisar y buscar la manera lo estoy escribiendo a medida q se me ocurre pero la idea esta jajaj

import logging as log
import RPi.GPIO as GPIO
import os

#PONER EN CONSTANTES O ALGUN LADO GENERAL
led = {}
led[1] = 4
led[2] = 17
ventilador = 23

log.basicConfig(filename='./action.log', filemode='w', level=log.DEBUG)

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
                        GPIO.output(led[int(command[2])], 1)
                        return "Luz " + command[2] +" encendida"
                else:
                        return "Dispositivo inexistente"
        elif(command[1] == "luces"):
                GPIO.output(led[1], 1)
                GPIO.output(led[2], 1)
                return "Luces encendidas"
                
        elif(command[1] == "ventilador"):
                GPIO.output(ventilador, 1)
                return "Ventilador encendido"
        else:
                return "Dispositivo inexistente"
	#logica para comunicarse con la rasp y prender el dispositivo deseado
	#comparar con el mapa de la casa
        	
	

def funcOff(command):
	print("funcOff")
	#logica para comunicarse con la rasp y apgar el dispositivo deseado
	#comparar con el mapa de la casa
        if(command[1] == "luz"):
                if(len(command)>2 and ( command[2]== "1" or command[2]== "2")):
                        GPIO.output(led[int(command[2])], 0)
                        return "Luz " + command[2] +" apagada"
                else:
                        return "Dispositivo inexistente"                
        elif(command[1] == "luces"):
                GPIO.output(led[1], 0)
                GPIO.output(led[2], 0)
                return "Luces apagadas"

        elif(command[1] == "ventilador"):
                GPIO.output(ventilador, 0)
                return "Ventilador apagado"
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

        else:
                return "Dispositivo inexistente"        

def funPhoto(command):
        print("funPhoto")
        os.system('fswebcam -q -r 320x240 -S 3 --no-banner --jpeg 50 --save ./images/photo.jpg') # uses Fswebcam to take picture
        return "photo"


listCommand = {
	'encender': funcOn,
	'apagar': funcOff,
	'activar': funcOn,
	'desactivar': funcOff,
        'estado': funState,
        'foto': funPhoto
}
