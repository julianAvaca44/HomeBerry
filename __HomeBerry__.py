print "WELCOME TO HOMEBERRY"
#aca va estar definido el main
#definir las configuraciones
#crear las instancias de cada modulo de mensajeria instantanea(WhatsApp, t Telegram)
from telegramModule import botTelegram as tb
from pymongo import MongoClient
import constantes as const
import threading
import time

client = MongoClient(const.MONGODB)
db = client.hbMongoDB

class myThread (threading.Thread):
    def __init__(self, type_process):
        threading.Thread.__init__(self)
        self.type = type_process
        #La siguiente linea hace que cuando se cierre un thread se cierren todos
        self.daemon = True
    def run(self):
        if(self.type == 1):
            tb.telegramBotRun(db)

def main():
        try:
            threadTelegram = myThread(1)
            threadTelegram.start()
            while(True): time.sleep(1)

        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    main()      
