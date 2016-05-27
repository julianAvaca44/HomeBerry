from yowsup.layers.interface                   import YowInterfaceLayer, ProtocolEntityCallback
import RPi.GPIO as GPIO

class EchoLayer(YowInterfaceLayer):

    luzEncendida1 = 0
    luzEncendida2 = 0
	
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        global luzEncendida1
        global luzEncendida2
        if messageProtocolEntity.getType() == 'text':
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(22, GPIO.OUT)
            GPIO.setup(17, GPIO.OUT)
            if messageProtocolEntity.getBody().lower() == 'luz':
                if self.luzEncendida1 == 1:
                    messageProtocolEntity.setBody("Luz encendida")
                else:   
                    messageProtocolEntity.setBody("Luz apagada")
            elif messageProtocolEntity.getBody().lower() == 'encender luz 1':
                if self.luzEncendida1 == 1:
                    messageProtocolEntity.setBody("La luz 1 ya estaba encendida")
                else:
                    GPIO.output(17,1)
                    messageProtocolEntity.setBody("Se encendio la luz 1")
                    self.luzEncendida1 = 1
            elif messageProtocolEntity.getBody().lower() == 'apagar luz 1':
                if self.luzEncendida1 == 0:
                    messageProtocolEntity.setBody("La luz 1 ya estaba apagada")
                else:
                    GPIO.output(17,0)
                    messageProtocolEntity.setBody("Se apago la luz 1")
                    self.luzEncendida1 = 0
            elif messageProtocolEntity.getBody().lower() == 'encender luz 2':
                if self.luzEncendida2 == 1:
                    messageProtocolEntity.setBody("La luz 2 ya estaba encendida")
                else:
                    GPIO.output(22,1)
                    messageProtocolEntity.setBody("Se encendio la luz 2")
                    self.luzEncendida2 = 1
            elif messageProtocolEntity.getBody().lower() == 'apagar luz 2':
                if self.luzEncendida2 == 0:
                    messageProtocolEntity.setBody("La luz 2ya estaba apagada")
                else:
                    GPIO.output(22,0)
                    messageProtocolEntity.setBody("Se apago la luz 2")
                    self.luzEncendida2 = 0
            elif messageProtocolEntity.getBody().lower() == 'encender luces':
                if self.luzEncendida1 == 1 and self.luzEncendida2 == 1:
                    messageProtocolEntity.setBody("Las luces estaban encendidas")
                else:
                    GPIO.output(17,1)
                    GPIO.output(22,1)
                    messageProtocolEntity.setBody("Se encendieron las luces")
                    self.luzEncendida1 = 1
                    self.luzEncendida2 = 1
            elif messageProtocolEntity.getBody().lower() == 'apagar luces':
                if self.luzEncendida1 == 0 and self.luzEncendida2 == 0:
                    messageProtocolEntity.setBody("Las luces estaban apagadas")
                else:
                    GPIO.output(17,0)
                    GPIO.output(22,0)
                    messageProtocolEntity.setBody("Se apagaron las luces")
                    self.luzEncendida1 = 0
                    self.luzEncendida2 = 0
            else:
                messageProtocolEntity.setBody("No te entiendo...")
            self.onTextMessage(messageProtocolEntity)
            
        elif messageProtocolEntity.getType() == 'media':
            self.onMediaMessage(messageProtocolEntity)

        self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))
        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))
        
    GPIO.cleanup()
    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())

    def onTextMessage(self,messageProtocolEntity):
        # just print info
        print("Echoing %s to %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))

    def onMediaMessage(self, messageProtocolEntity):
        # just print info
        if messageProtocolEntity.getMediaType() == "image":
            print("Echoing image %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.getMediaType() == "location":
            print("Echoing location (%s, %s) to %s" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(), messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.getMediaType() == "vcard":
            print("Echoing vcard (%s, %s) to %s" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(), messageProtocolEntity.getFrom(False)))
        elif messageProtocolEntity.getMediaType() == "voice" :
            print("Mensaje de voz")
