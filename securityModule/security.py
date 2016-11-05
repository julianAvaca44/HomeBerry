#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint
import time
import re
import constantes as const

def checkUserProfileAcces(user, commands, db):
	if(user['perfil'] == "adulto"):
		return True
	elif(commands[1] ==  const.DISP_LUCES or 
		commands[1] ==  const.DISP_LUZ or 
		commands[1] ==  const.DISP_VENTILADOR):
			return True
	else:
		return False
		

def checkUser(number, db):
	print "checkUser"
	print number
	usr = db.users.find_one({const.MONOGO_TELEFONO:int(number)})
	if usr == None:
		numberAux = number[:2] + "9" + number[2:]
		usr = db.users.find_one({const.MONOGO_TELEFONO:int(numberAux)})
		if usr == None:
			numberAux = number[:2] + number[3:]
			usr = db.users.find_one({const.MONOGO_TELEFONO:int(numberAux)})	
			if usr == None:	
				usr = db.users.find_one({const.MONOGO_TELEFONO:number})
				if usr == None:
					numberAux = number[:2] + "9" + number[2:]
					usr = db.users.find_one({const.MONOGO_TELEFONO:numberAux})
					if usr == None:
						numberAux = number[:2] + number[3:]
						usr = db.users.find_one({const.MONOGO_TELEFONO:numberAux})					
	return usr
	
def checkUserTelegram(telegramId, db):
	return db.users.find_one({'telegramId':telegramId})
	
def checkUserSession(user, msg, db):
	if ((int(time.time()) - user['ultimaSolicitudCoordenadas']) > 86400):
		regex = re.compile(r'[1-9][1-9](;)[1-9][1-9]')				
		if(bool(regex.match(msg))):
			values = msg.split(";",1)
			request = user['coordSolicitadas'].split(";",1)
			print user['tc']
			if(int(user[const.MONOGO_TARJETA_COORDENADAS]['values'][request[0]]) == int(values[0]) and int(user[const.MONOGO_TARJETA_COORDENADAS]['values'][request[1]]) == int(values[1])):
				result = db.users.update_one({"_id":user['_id']}, {"$set":{'ultimaSolicitudCoordenadas':int(time.time()),
																		   'coordSolicitadas':''}})
				return 'Comprobación realizada correctamente. Ingrese comando'
																				
			else:
				return 'Datos incorrectos. Indicar las posiciones ' + request[0] + ' y ' + request[1] + ' de la tarjeta de coordenadas separadas por ;'
				
		else:
			pos1 = chr(ord('A') + randint(0,8)) + str(randint(1,9))
			pos2 = chr(ord('A') + randint(0,8)) + str(randint(1,9))
			message_to_send = 'Indicar las posiciones ' + pos1 + ' y ' + pos2 + ' de la tarjeja te coordenadas separadas por ;'
			result = db.users.update_one({"_id":user['_id']}, {"$set":{'coordSolicitadas':pos1+';'+pos2}})
			#print "Respuesta: " + str(user['tarjeta_coordenadas'][pos1]) + ';'+ user[pos2][request[0]]
			return message_to_send
	else:
		return 'OK'

def getNewCoordinatesCard(number, db):
	user = checkUser(number, db)
	if(user <> None):
		coordinatesCard={'A1':0}
		for i in range(1, 10):
			for j in range(1, 10):
				coordinatesCard[chr(ord('A') + i - 1) + str(j)] = randint(0,99)	

		print ('A1: %02d, A2: %02d, A3: %02d, A4: %02d, A5: %02d, A6: %02d, A7: %02d, A8: %02d, A9: %02d' % (coordinatesCard["A1"], coordinatesCard["A2"], coordinatesCard["A3"], coordinatesCard["A4"], coordinatesCard["A5"], coordinatesCard["A6"], coordinatesCard["A7"], coordinatesCard["A8"], coordinatesCard["A9"]))
		print ('B1: %02d, B2: %02d, B3: %02d, B4: %02d, B5: %02d, B6: %02d, B7: %02d, B8: %02d, B9: %02d' % (coordinatesCard["B1"], coordinatesCard["B2"], coordinatesCard["B3"], coordinatesCard["B4"], coordinatesCard["B5"], coordinatesCard["B6"], coordinatesCard["B7"], coordinatesCard["B8"], coordinatesCard["B9"]))
		print ('C1: %02d, C2: %02d, C3: %02d, C4: %02d, C5: %02d, C6: %02d, C7: %02d, C8: %02d, C9: %02d' % (coordinatesCard["C1"], coordinatesCard["C2"], coordinatesCard["C3"], coordinatesCard["C4"], coordinatesCard["C5"], coordinatesCard["C6"], coordinatesCard["C7"], coordinatesCard["C8"], coordinatesCard["C9"]))
		print ('D1: %02d, D2: %02d, D3: %02d, D4: %02d, D5: %02d, D6: %02d, D7: %02d, D8: %02d, D9: %02d' % (coordinatesCard["D1"], coordinatesCard["D2"], coordinatesCard["D3"], coordinatesCard["D4"], coordinatesCard["D5"], coordinatesCard["D6"], coordinatesCard["D7"], coordinatesCard["D8"], coordinatesCard["D9"]))
		print ('E1: %02d, E2: %02d, E3: %02d, E4: %02d, E5: %02d, E6: %02d, E7: %02d, E8: %02d, E9: %02d' % (coordinatesCard["E1"], coordinatesCard["E2"], coordinatesCard["E3"], coordinatesCard["E4"], coordinatesCard["E5"], coordinatesCard["E6"], coordinatesCard["E7"], coordinatesCard["E8"], coordinatesCard["E9"]))
		print ('F1: %02d, F2: %02d, F3: %02d, F4: %02d, F5: %02d, F6: %02d, F7: %02d, F8: %02d, F9: %02d' % (coordinatesCard["F1"], coordinatesCard["F2"], coordinatesCard["F3"], coordinatesCard["F4"], coordinatesCard["F5"], coordinatesCard["F6"], coordinatesCard["F7"], coordinatesCard["F8"], coordinatesCard["F9"]))
		print ('G1: %02d, G2: %02d, G3: %02d, G4: %02d, G5: %02d, G6: %02d, G7: %02d, G8: %02d, G9: %02d' % (coordinatesCard["G1"], coordinatesCard["G2"], coordinatesCard["G3"], coordinatesCard["G4"], coordinatesCard["G5"], coordinatesCard["G6"], coordinatesCard["G7"], coordinatesCard["G8"], coordinatesCard["G9"]))
		print ('H1: %02d, H2: %02d, H3: %02d, H4: %02d, H5: %02d, H6: %02d, H7: %02d, H8: %02d, H9: %02d' % (coordinatesCard["H1"], coordinatesCard["H2"], coordinatesCard["H3"], coordinatesCard["H4"], coordinatesCard["H5"], coordinatesCard["H6"], coordinatesCard["H7"], coordinatesCard["H8"], coordinatesCard["H9"]))
		print ('I1: %02d, I2: %02d, I3: %02d, I4: %02d, I5: %02d, I6: %02d, I7: %02d, I8: %02d, I9: %02d' % (coordinatesCard["I1"], coordinatesCard["I2"], coordinatesCard["I3"], coordinatesCard["I4"], coordinatesCard["I5"], coordinatesCard["I6"], coordinatesCard["I7"], coordinatesCard["I8"], coordinatesCard["I9"]))
						
		result = db.users.update_one({"_id":user['_id']},
							 {"$set":
							  {const.MONOGO_TARJETA_COORDENADAS .values:{
								"A1":coordinatesCard["A1"],
								"A2":coordinatesCard["A2"],
								"A3":coordinatesCard["A3"],
								"A4":coordinatesCard["A4"],
								"A5":coordinatesCard["A5"],
								"A6":coordinatesCard["A6"],
								"A7":coordinatesCard["A7"],
								"A8":coordinatesCard["A8"],
								"A9":coordinatesCard["A9"],

								"B1":coordinatesCard["B1"],
								"B2":coordinatesCard["B2"],
								"B3":coordinatesCard["B3"],
								"B4":coordinatesCard["B4"],
								"B5":coordinatesCard["B5"],
								"B6":coordinatesCard["B6"],
								"B7":coordinatesCard["B7"],
								"B8":coordinatesCard["B8"],
								"B9":coordinatesCard["B9"],

								"C1":coordinatesCard["C1"],
								"C2":coordinatesCard["C2"],
								"C3":coordinatesCard["C3"],
								"C4":coordinatesCard["C4"],
								"C5":coordinatesCard["C5"],
								"C6":coordinatesCard["C6"],
								"C7":coordinatesCard["C7"],
								"C8":coordinatesCard["C8"],
								"C9":coordinatesCard["C9"],

								"D1":coordinatesCard["D1"],
								"D2":coordinatesCard["D2"],
								"D3":coordinatesCard["D3"],
								"D4":coordinatesCard["D4"],
								"D5":coordinatesCard["D5"],
								"D6":coordinatesCard["D6"],
								"D7":coordinatesCard["D7"],
								"D8":coordinatesCard["D8"],
								"D9":coordinatesCard["D9"],

								"E1":coordinatesCard["E1"],
								"E2":coordinatesCard["E2"],
								"E3":coordinatesCard["E3"],
								"E4":coordinatesCard["E4"],
								"E5":coordinatesCard["E5"],
								"E6":coordinatesCard["E6"],
								"E7":coordinatesCard["E7"],
								"E8":coordinatesCard["E8"],
								"E9":coordinatesCard["E9"],

								"F1":coordinatesCard["F1"],
								"F2":coordinatesCard["F2"],
								"F3":coordinatesCard["F3"],
								"F4":coordinatesCard["F4"],
								"F5":coordinatesCard["F5"],
								"F6":coordinatesCard["F6"],
								"F7":coordinatesCard["F7"],
								"F8":coordinatesCard["F8"],
								"F9":coordinatesCard["F9"],

								"G1":coordinatesCard["G1"],
								"G2":coordinatesCard["G2"],
								"G3":coordinatesCard["G3"],
								"G4":coordinatesCard["G4"],
								"G5":coordinatesCard["G5"],
								"G6":coordinatesCard["G6"],
								"G7":coordinatesCard["G7"],
								"G8":coordinatesCard["G8"],
								"G9":coordinatesCard["G9"],

								"H1":coordinatesCard["H1"],
								"H2":coordinatesCard["H2"],
								"H3":coordinatesCard["H3"],
								"H4":coordinatesCard["H4"],
								"H5":coordinatesCard["H5"],
								"H6":coordinatesCard["H6"],
								"H7":coordinatesCard["H7"],
								"H8":coordinatesCard["H8"],
								"H9":coordinatesCard["H9"],

								"I1":coordinatesCard["I1"],
								"I2":coordinatesCard["I2"],
								"I3":coordinatesCard["I3"],
								"I4":coordinatesCard["I4"],
								"I5":coordinatesCard["I5"],
								"I6":coordinatesCard["I6"],
								"I7":coordinatesCard["I7"],
								"I8":coordinatesCard["I8"],
								"I9":coordinatesCard["I9"]                                  
							  }
		}})

