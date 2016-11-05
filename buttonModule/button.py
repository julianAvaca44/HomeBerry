#!/usr/bin/env python
# -*- coding: utf-8 -*-

from actionModule import action
import RPi.GPIO as GPIO
import time


def buttonHandle(db):
    actm = action.action(db, None)

    buttons = db.devices.find({'tipo':'boton'})
    
    while True:
        buttonPushed = 0
        buttonPushedZone = ""
        #GPIO.wait_for_edge(botonEncenderLed11, GPIO.RISING)
        for i in range(0, buttons.count()):
			if(GPIO.input(int(buttons[i]['pin'])) == False):
				buttonPushed = int(buttons[i]['numero'])
				buttonPushedZone = buttons[i]['idZona']
				

        if(buttonPushed>0):
            device = db.devices.find_one({'tipo':'luz', 'numero':buttonPushed, 'idZona':buttonPushedZone})

            state = GPIO.input(int(device['pin']))
            if(state == True):
				#print 'apagar luz' + buttonPushed + ' zona ' + buttonPushedZone
				commandList = ["apagar", "luz", str(buttonPushed), buttonPushedZone]
            else:
				#print 'prender luz' + buttonPushed + ' zona ' + buttonPushedZone
				commandList = ["encender", "luz", str(buttonPushed), buttonPushedZone]
            actm.acction(commandList)
            time.sleep(0.5)
        else:
            time.sleep(0.1)
            	
	    #buttons = db.devices.find({'tipo':'boton'})

