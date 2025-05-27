# -*- encoding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import csv, time
from naoqi import ALProxy

# --- CONFIGURACIÓN ---
ip = "192.168.190.85"
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
    print(">>> ALSpeechRecognition no disponible. ")
    habla.say("El reconocimiento de voz no está disponible.")
    modo_voz = False

#Inicio de la actividad
movimiento.wakeUp()
movimiento.setFallManagerEnabled(True)

habla.say("¡Lo tengo chicos! Este es el cuadro que he creado con las palabras que habéis elegido. ¿Qué os parece?")

time.sleep(10)

habla.say("Espero que os haya gustado mucho esta actividad. Yo estoy muy contento de haber pasado este rato con " \
"vosotros, y os estoy muy agradecido. Sin vuestra ayuda, no podría haber recuperado mi memoria!!")

habla.say("Espero que la próxima vez que vayáis a un museo os acordéis de mi y de la manera en la que hemos " \
"analizado el cuadro. Yendo por partes y fijándosed en los detalles, ningún cuadro será rival para vosotros.")

time.sleep(3)

habla.say("Espero que volvamos a vernos pronto. Muchas gracias chicos!")

movimiento.rest()