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
            wa.WhatsAppBot().start(self.db)
        elif(self.type == 2):
            tb.telegramBotRun(self.db)
        elif(self.type == 3):
            btn.buttonHandle(self.db)#EVENTOS EXTERNOS

def main():
   
        try:
			client = MongoClient()                        
			db = client.HomeBerry
			threadWhatsApp = myThread(1, db)
			threadTelegram = myThread(2, db)
			threadBoton = myThread(3, db)
			setupGPIO(db)
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
	for device in devices:
		print device['tipo']
		if(device['tipo'].lower() == 'luz' 
		          or device['tipo'].lower() == 'ventilador'
		          or device['tipo'].lower() == 'buzzer'):
			GPIO.setup(int(device['pin']), GPIO.OUT)
		elif(device['tipo'].lower() == 'boton'):
			GPIO.setup(int(device['pin']), GPIO.IN, GPIO.PUD_UP)
		elif(device['tipo'].lower() == 'sensorluz' 
		          or device['tipo'].lower() == 'sensorpuerta'):
			GPIO.setup(int(device['pin']), GPIO.IN)

if __name__ == '__main__':
    main()

    
