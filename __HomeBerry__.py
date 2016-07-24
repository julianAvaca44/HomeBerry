#aca va estar definido el main
#definir las configuraciones
#crear las instancias de cada modulo de mensajeria instantanea(WhatsApp, t Telegram)
from telegramModule import botTelegram as tb
from whatsAppModule import whatsapp as wa
from buttonModule import button as btn
from pymongo import MongoClien
import threading
import RPi.GPIO as GPIO

import time

class myThread (threading.Thread):
    def __init__(self, type_process):
        threading.Thread.__init__(self)
        self.type = type_process
        #La siguiente linea hace que cuando se cierre un thread se cierren todos
        self.daemon = True
    def run(self):
        if(self.type == 1):
            wa.WhatsAppBot().start()
        elif(self.type == 2):
            tb.telegramBotRun()
        elif(self.type == 3):
            btn.buttonHandle()



def main():
   
        try:
            threadWhatsApp = myThread(1)
            threadTelegram = myThread(2)
            threadBoton = myThread(3)
            
            threadWhatsApp.start()
            threadTelegram.start()
            threadBoton.start()
            while(True): time.sleep(1)

        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()

    
