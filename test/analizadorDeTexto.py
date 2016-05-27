# -*- coding: utf-8 -*-
import unicodedata
import time
import os


def normalize_string(mystring):
        mystring.encode("utf-8")
        text = unicodedata.normalize("NFKD", mystring)
        clean_text = text.encode("ascii", "ignore")
        return clean_text

def action(instruction, sender_name):
	resp_string = "¡No te entiendo capo!. Pedime las opciónes si no te acordás."

	if "hola" in instruction.lower() or "mostri" in instruction.lower():
	    resp_string = "¡Hola, %s!, ¿Que necesitas?" % sender_name
	elif "quien sos" in instruction.lower() or "como te llamas" in instruction.lower():
	    resp_string = "Soy Marta, trabajo acá."
	elif "opciones" in instruction.lower():
	    resp_string = "Puedo manejar la alarma y el aire acondicionado. Buscar información en Wikipedia y noticias en Twiter. Darte mi dirección IP y el tiempo estimado al trabajo. Puedo manejar tu lista de recordatorios."
	return resp_string







