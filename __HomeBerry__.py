#aca va estar definido el main
#definir las configuraciones
#crear las instancias de cada modulo de mensajeria instantanea(WhatsApp, t Telegram)
from telegramModule import botTelegram as tb
from whatsAppModule import whatsapp as wa
from buttonModule import button as btn
import threading

import time

class myThread (threading.Thread):
    def __init__(self, type_process):
        threading.Thread.__init__(self)
        self.type = type_process
    def run(self):
        if(self.type == 1):
            wa.WhatsAppBot().start()
        elif(self.type == 2):
            tb.telegramBotRun()
        elif(self.type == 3):
            btn.buttonHandle()



def main():
	#TODO:crear instancias de los bot, cliente, o conexiones de telegram y/o whatsApp
	#todo crear a telegramBotRun como una clase y ejecutar una instancia de la misma
	#otro ver como armar otro hilo
    
    
        thread1 = myThread(1)
        thread2 = myThread(2)
        thread3 = myThread(3)
        
        thread1.start()
        thread2.start()
        thread3.start()
    



    

if __name__ == '__main__':
    main()

    
