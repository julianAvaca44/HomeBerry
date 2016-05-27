
#objetivo del messeage analizador es parsear un mensaje sea 
#en formato de audio, texto, imagenes o algun otro soporte y parsear lo a un comando posible
#en caso que no se pueda resolver el parseo informar que no se pudo comprender el mensaje
#analiza la sintaxis de mensaje
#lo formatea: lo pasa a minuscula, deberia eleminar el resto de caracteres no deseados, y pasarlo a codificacion utf-8
import re #libreria para las regex
import constantes as const

def analizarMessage(message):
	regex = re.compile(const.REGEXCOMMANDS)
	reCommand = regex.findall(message)
	#limpio el array de commandos
	if (len(reCommand)<1):
		return None
	commandList = [elem for elem in reCommand[0] if elem !='']
	commandList.pop(0) #elimino los matches padres
	if (len(commandList)>2):
		commandList.pop(2) #elimino los matches padres
	return commandList


"""
def convertSpeechToText(message,fileId,file):
	try:
	    logger.info("New audio message\nFrom: %s\nchat_id: %d\nText: %s Audio: %s" %
	                (message.from_user,
	                 message.chat_id,
	                 message.text, fileId))
	    # Download Audio Message 
	    newFile = file
	    newFile.download('message.ogg')
	    # Convert Ogg to Wav
	    os.system('/usr/bin/opusdec message.ogg message.wav')
	    message = f.SpeechToText('message.wav')#modulo para convertir audio
	    logger.info("Speech Recognition: %s" % message)
	#If couldn't transform audio in text 
	except:
    	logger.info("New text message\nFrom: %s\nchat_id: %d\nText: %s" %
        	        (update.message.from_user,
            	     update.message.chat_id,
                	 update.message.text))
    	message = "perdon no pero no pude interpretar tu audio :("
    return message
"""
"""
def SpeechToText(filename):
	#!/usr/bin/env python3
	import speech_recognition as sr
	from os import path
	WAV_FILE = path.join(path.dirname(path.realpath(__file__)), filename)
	r = sr.Recognizer()
	with sr.WavFile(WAV_FILE) as source:
	    audio = r.record(source) # read the entire WAV file
        
	# recognize speech using Google Speech Recognition
	try:
	    # for testing purposes, we're just using the default API key
	    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
	    # instead of `r.recognize_google(audio)`
	    recognized_word = normalize_string(r.recognize_google(audio, language = "es-US"))
	    print("Google Speech Recognition thinks you said: " + recognized_word)
	    return recognized_word
	except sr.UnknownValueError:
	    caca = "Google Speech Recognition could not understand audio"
            return caca
	except sr.RequestError as e:
	    caca = "Could not request results from Google Speech Recognition service; {0}".format(e)
            return caca

#f.normalize_string(update.message.from_user['first_name'])
def normalize_string(mystring):
        mystring.encode("utf-8")
        text = unicodedata.normalize("NFKD", mystring)
        clean_text = text.encode("ascii", "ignore")
        return clean_text
"""