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
        GPIO.wait_for_edge(boton_encender, GPIO.RISING)
        state = GPIO.input(led)
        if(state == True):
            #print("Estaba encendido")
            commandList = ["apagar", "luz"]
        else:
            #print("Estaba apagado")
            commandList = ["encender", "luz"]
        actm.acction(commandList)
        time.sleep(0.5)
