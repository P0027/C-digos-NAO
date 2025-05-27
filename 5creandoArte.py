# -*- encoding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
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
    print(">>> ALSpeechRecognition no disponible.")
    habla.say("El reconocimiento de voz no está disponible.")
    modo_voz = False

#Explicacion actividad
movimiento.wakeUp()
movimiento.setFallManagerEnabled(True)

habla.say("Tengo que daros las gracias por vuestra ayuda. Estoy seguro de que sin ella no podría" \
"haber recuperado la memoria. Además, gracias a recordar el significado de uno de mis cuadros" \
"favoritos, creo que mi inspiración ha vuelto por fin.")

habla.say("¿No me creéis? Pues os lo voy a demostrar.")

habla.say("Solo dejadme pensar, a ver si se me ocurre cómo podemos hacerlo...")

time.sleep(5)

habla.say("¡Lo tengo! Chicos, necesito que cada grupo elija una palabra relacionada " \
"con una temática. El grupo A deberá decirme un lugar, el grupo b un animal, el grupo c una estación del año" \
"y el grupo D un sentimiento, y en base a eso yo crearé mi obra. ¿Qué os parece?")

time.sleep(5)

habla.say("¡Genial! Entonces, os dejo unos minutos para pensar.")

postura.goToPosture("Sit", 0.8)
time.sleep(300)
postura.goToPosture("StandInit", 0.8)

habla.say("¿Estáis listos? Decid vuestra palabra")

raw_input("Presiona enter")

habla.say("¡Muchas gracias! Ahora, necesito unos minutos para pensar. Cuando tenga mi cuadro, os lo enseño")

movimiento.rest()
