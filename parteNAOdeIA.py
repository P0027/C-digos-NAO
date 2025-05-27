# -*- encoding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


import json
import requests
from naoqi import ALProxy


# Dirección del servidor Flask
server_url = "http://127.0.0.1:5000/ask"

robot_ip = "192.168.255.85"  # Cambia esto por la IP de tu robot NAO
robot_port = 9559

# Conexión con el módulo de TTS (Text to Speech) de NAOqi
tts = ALProxy("ALTextToSpeech", robot_ip, robot_port)

while True:
    question = raw_input("Haz una pregunta a la IA (o escribe 'salir' para terminar): ")
    if question.lower() == "salir":
        break

    # Enviar la pregunta al servidor Flask
    response = requests.post(server_url, json={"question": question})
    
    if response.status_code == 200:
        answer = response.json()["response"].decode("utf-8")  # Garantiza que se maneje bien la codificación
        print("IA:", answer.encode("utf-8"))
        tts.say(answer.encode('utf-8')) 

    else:
        print("Error en la respuesta de la IA")
