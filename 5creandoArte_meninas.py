# -*- encoding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
from naoqi import ALProxy

# --- CONFIGURACIÓN ---
ip = "192.168.174.85"
puerto = 9559
servidorAI = "http://127.0.0.1:5000/ask"
archivoRespuestas = "resultados_detectivesArte.csv"

# Inicializar proxies
movimiento = ALProxy("ALMotion", ip, puerto)
postura = ALProxy("ALRobotPosture", ip, puerto)
habla = ALProxy("ALAnimatedSpeech", ip, puerto)
tts = ALProxy("ALTextToSpeech", ip, puerto)
tts.setLanguage("Spanish")

# Intentar inicializar reconocimiento de voz
modo_voz = True
try:
    escucha = ALProxy("ALSpeechRecognition", ip, puerto)
    memoria = ALProxy("ALMemory", ip, puerto)
except RuntimeError:
    print(">>> ALSpeechRecognition no disponible.")
    habla.say("El reconocimiento de voz no está disponible. ")
    modo_voz = False

#
postura.goToPosture("StandInit", 0.8)

habla.say("¿Estáis listos? Decid vuestra palabra")

raw_input("Presiona enter")

habla.say("¡Muchas gracias! Ahora, necesito unos minutos para pensar. Cuando tenga mi cuadro, os lo enseño")

movimiento.rest()
