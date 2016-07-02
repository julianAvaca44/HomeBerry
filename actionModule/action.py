#Obejtivo del action: recibe un comando y lo ejecuta
#es el encargado de comunicarse con las raspberry pi 3
#caso de algun fallo comunicar lo
# la idea de cuando llega un comando que analize un objecto con la siguiente estructura



import logging as log
import constantes as const
#import RPi.GPIO as GPIO

log.basicConfig(filename='./action.log', filemode='w', level=log.DEBUG)

def acction(command,db):
	if command == None:
		return "No se reconoce el commando"	
	elif command[0] in listCommand.keys(): 
		return listCommand[command[0]](command,db)
	else:
		return "Comando no valido" 

		
def funcOn(command,db):
	print "_____________________-_____________________"
	print "-- funcion On --"
	devices = db.devices.find({'tipo':command[1]})
	#for dev in devices:
		#print dev
	if(len(command) == 4):
		print command[1] + " - " + command[2] + " - " + command[3]
		device = db.devices.find_one({'tipo':command[1],'numero':int(command[2]),'idZona':command[3]})		
		#device = db.devices.find_one({'tipo':'luz','numero':1,'idZona':'Z1'})		
		print str(int(device['estado']))
		if(device == None):
			return "dispositivo inexistente"
		elif(int(device['estado']) != 0):
			return device['tipo'] + " - " + str(device['numero']) + ": se encontraba encendida"
		else:
			db.devices.update_one({'tipo':command[1],'numero':int(command[2]),'idZona':command[3]},
				{'$set':{'estado':1}})
			return "dispositivio encendido"
	#logica para comunicarse con la rasp y prender el dispositivo deseado
	#comparar con el mapa de la casa
	

"""
	print("funcOn")
	if(command[1] == "luz"):
		if(len(command)>2 and ( command[2]== "1" or command[2]== "2")):
			if (GPIO.input(led[int(command[2])]) == False): aca le paso el pin donde esta ubicado
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
"""




def funcOff(commando, db):
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
