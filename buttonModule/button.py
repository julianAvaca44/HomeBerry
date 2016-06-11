#!/usr/bin/env python
# -*- coding: utf-8 -*-

from actionModule import action as actm
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#pin temporal
#ESTO DEBERIA ESTAR EN UN ARCH DE CONFIGURACION QUE SE USA AL INICIO
led = {}
led[1] = 4
led[2] = 17
botonEncenderLed1 = 27
botonEncenderLed2 = 22
ventilador = 23


GPIO.setup(botonEncenderLed1, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(botonEncenderLed2, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(led[1], GPIO.OUT)
GPIO.setup(led[2], GPIO.OUT)
GPIO.setup(ventilador, GPIO.OUT)

def buttonHandle():
    while True:
        botonPresionado = 0
        #GPIO.wait_for_edge(botonEncenderLed11, GPIO.RISING)
        if (GPIO.input(botonEncenderLed1) == False):
            botonPresionado = 1
        elif (GPIO.input(botonEncenderLed2) == False):
            botonPresionado = 2

        if(botonPresionado>0):
            state = GPIO.input(led[botonPresionado])
            if(state == True):
                commandList = ["apagar", "luz", str(botonPresionado)]
            else:
                commandList = ["encender", "luz", str(botonPresionado)]
            actm.acction(commandList)
            time.sleep(0.5)
        else:
            time.sleep(0.1)
