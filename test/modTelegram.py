#!usr/bin/env
import pexpect
 
contacto = "Javi_Cescon"                          #Contacto a quien va el mensaje
mensaje = "Hola javi te escribo desde un programa de python, que usa de fondo el clinete-Telegram!!"              #Mensaje a enviar
telegram = pexpect.spawn('../../TelegramProject/tg/bin/telegram-cli -k tg-server.pub') #Inicia Telegram
telegram.expect('0m')                            #Espera a que termine de iniciar
telegram.sendline('msg '+contacto+' '+mensaje)   #Ejecuta el comando msg
print ('Mensaje enviado a '+ contacto)           #Notifica que ya se ha mandado el mensaje
telegram.sendline('quit')                        #cierra Telegram