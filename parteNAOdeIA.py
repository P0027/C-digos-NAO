# -*- encoding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from naoqi import ALProxy


servidor = "http://127.0.0.1:5000/ask"

ip = "192.168.255.85" 
puerto = 9559

tts = ALProxy("ALTextToSpeech", ip, puerto)

while True:
    pregunta = raw_input("Haz una pregunta a la IA (o escribe 'salir' para terminar): ")
    if pregunta.lower() == "salir":
        break

    # Enviar la pregunta
    respuesta = requests.post(servidor, json={"pregunta": pregunta})
    
    if respuesta.status_code == 200:
        respuesta = respuesta.json()["respuesta"].decode("utf-8")
        print("IA:", respuesta.encode("utf-8"))
        tts.say(respuesta.encode('utf-8')) 

    else:
        print("Error en la respuesta de la IA")
