#!/usr/bin/env python
# -*- coding: utf-8 -*-

from actionModule import action as actm
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#pin temporal
#ESTO DEBERIA ESTAR EN UN ARCH DE CONFIGURACION QUE SE USA AL INICIO
led = 4
boton_encender = 18

GPIO.setup(boton_encender, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(led, GPIO.OUT)

def buttonHandle():
    while True:
        if GPIO.input(boton_encender) == False:        
            commandList = ["encender", "luz"]
            actm.acction(commandList)
	time.sleep(0.5) 
