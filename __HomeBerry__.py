#aca va estar definido el main
#definir las configuraciones
#crear las instancias de cada modulo de mensajeria instantanea(WhatsApp, t Telegram)
from telegramModule import botTelegram as tb

def main():
	#TODO:crear instancias de los bot, cliente, o conexiones de telegram y/o whatsApp
	#todo crear a telegramBotRun como una clase y ejecutar una instancia de la misma
	#otro ver como armar otro hilo
	tb.telegramBotRun()

if __name__ == '__main__':
    main()