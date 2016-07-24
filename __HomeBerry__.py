print "WELCOME TO HOMEBERRY"
#aca va estar definido el main
#definir las configuraciones
#crear las instancias de cada modulo de mensajeria instantanea(WhatsApp, t Telegram)
from telegramModule import botTelegram as tb
from whatsAppModule import whatsapp as wa
from buttonModule import button as btn
from pymongo import MongoClient
import threading
import RPi.GPIO as GPIO

import time


class myThread (threading.Thread):
    def __init__(self, type_process, db):
        threading.Thread.__init__(self)
        self.type = type_process
        #La siguiente linea hace que cuando se cierre un thread se cierren todos
        self.daemon = True
        self.db = db
    def run(self):
        if(self.type == 1):
            wa.WhatsAppBot().start()
        elif(self.type == 2):
            tb.telegramBotRun(self.db)
        elif(self.type == 3):
            btn.buttonHandle()

def main():
   
        try:
			client = MongoClient()                        
			db = client.homeBerryDB
			threadWhatsApp = myThread(1, db)
			threadTelegram = myThread(2, db)
			threadBoton = myThread(3, db)
            
			threadWhatsApp.start()
			threadTelegram.start()
			threadBoton.start()
			while(True): time.sleep(1)

        except KeyboardInterrupt:
            pass


def setupGPIO(db):
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	devices = db.devices.find()
	for i in range(0, devices.count()):
		if(devices[i]['tipo'].lower() == 'luz' or devices[i]['tipo'].lower() == 'ventilador'):
			GPIO.setup(int(devices[i]['pin']), GPIO.OUT)
		elif(devices[i]['tipo'].lower() == 'boton'):
			GPIO.setup(int(devices[i]['pin']), GPIO.IN, GPIO.PUD_UP)
		elif(devices[i]['tipo'].lower() == 'sensorluz'):
			GPIO.setup(int(devices[i]['pin']), GPIO.IN)


if __name__ == '__main__':
    main()

    
