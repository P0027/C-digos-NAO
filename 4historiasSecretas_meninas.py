# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#Librerías
from naoqi import ALProxy
import time, random

# Configuración
ip = "192.168.174.85"
puerto = 9559

# Inicializar proxies

movimiento = ALProxy("ALMotion", ip, puerto)
habla = ALProxy("ALAnimatedSpeech", ip, puerto)
tts = ALProxy("ALTextToSpeech", ip, puerto)
postura = ALProxy("ALRobotPosture", ip, puerto)
vida = ALProxy("ALAutonomousLife", ip, puerto)
vida.setState("disabled")
tts.setLanguage("Spanish")

# Intentar inicializar reconocimiento de voz
modo_voz = True
try:
    reconocedor = ALProxy("ALSpeechRecognition", ip, puerto)
    memoria = ALProxy("ALMemory", ip, puerto)
except RuntimeError:
    print(">>> ALSpeechRecognition no disponible.")
    habla.say("El reconocimiento de voz no está disponible.")
    modo_voz = False

#Introducción de la actividad.
movimiento.wakeUp()
movimiento.setFallManagerEnabled(True)


habla.say("Chicos, creo que ya recuerdo el verdadero significado del cuadro." \
"¿Qué os parece si lo reconstruimos entre todos?")

habla.say("Estamos en una sala del palacio real, en el año 1656. Es un día cualquiera, pero hay algo especial... ¿Quién creéis que es la niña que está en el centro?")
raw_input("Pulsa Enter para que el robot continúe...")
habla.say("Fenomenal")
time.sleep(2)

habla.say("Un poco más atrás, vemos a un hombre con pinceles en la mano. Tiene una mirada seria, como si estuviera muy concentrado. ¿Sabéis quién es?")
raw_input("Pulsa Enter para que el robot continúe...")
habla.say("Muy bien")
time.sleep(2)

habla.say("Ahora miramos al fondo... hay una puerta abierta. En ella aparece un hombre, quieto, como si estuviera observando. ¿Qué creéis que está mirando?")
raw_input("Pulsa Enter para que el robot continúe...")
habla.say("Así se hace")
time.sleep(2)

habla.say("Y justo al fondo hay un espejo. Refleja a dos personas. ¿Quiénes pueden ser?")
raw_input("Pulsa Enter para que el robot continúe...")
habla.say("Ahí va la última")
time.sleep(2)

habla.say("Más o menos ya sabemos todo lo que está ocurriendo. Parece que en la escena hay más cosas de las que nosotros como espectadores podemos ver. ¿Alguien sabría decirme qué es lo que está ocurriendo realmente en la escena?")
raw_input("Pulsa Enter para que el robot continúe...")
habla.say("Ahí va la última")
time.sleep(2)




habla.say("Creo que ya lo recuerdo todo! Fijaos bien! Lo importante de esta escena no es solo lo que vemos en el cuadro, sino cómo lo miramos. En realidad es un juego de perpectivas. En el cuadro, estamos viendo lo que ven los reyes mientras están siendo retratados. Es por eso que podemos ver su reflejo en el espejo." \
"Los reyes, padres de la infanta, la chica rubia que aparece en el centro del cuadro, están siendo retratados por el pintor, Velázquez. Mientras tanto, toda la corte los mira atentamente. La infanta parece atenta a sus padres, pues probablemente la siguiente en ser retratada será ella. Las meninas cuidan de ella." \
"Incluso el perro, la mascota de la familia, ha acudido a la reunión! Aunque si os fijáis, el bufón está intentando echarlo... El hombre que aparece al fondo es un trabajador de la corte, que observa la escena desde lejos")
time.sleep(2)

habla.say("Lo que Velázquez pintó no fue solo una escena cualquiera, sino un verdadero juego visual. Como si hubiera escondido pistas por todo el cuadro para que nosotros, al mirarlo con atención, pudiéramos descubrir lo que está pasando poco a poco." \
"Nos muestra a los reyes sin pintarlos directamente. Nos pone en su lugar. Nos hace pensar que tal vez nosotros también estamos dentro del cuadro, siendo observados." \
"Con cada detalle —el espejo, las miradas, la puerta al fondo— nos invita a mirar más allá, a no quedarnos solo con lo que vemos a primera vista.")

time.sleep(2)

habla.say("Velázquez no solo quería pintar a la familia real. El pintor ya los retrató en otras ocasiones, como podemos ver en la imagen que os está mostrando Paula.")

time.sleep(3)

habla.say(" Con esta obra, el pintor quería hacernos pensar. Quería que nos preguntáramos: ¿quién mira a quién?, ¿qué está dentro y qué está fuera del cuadro?, ¿qué es real y qué es reflejo?" \
"Y al final, como en los buenos juegos, la respuesta no está escrita... está en lo que cada uno descubre al observar con calma.")

habla.say("Por eso, os animo a que la próxima vez que tengáis un problema que no sepáis solucionar, o alguna tarea que no consigáis entender, pongáis en práctica lo que hemos hecho hoy." \
"Tomaron un momento para fijaron en todos los detalles, y así todo será más fácil de resolver")

time.sleep(2)

habla.say("Muchas gracias chicos, espero que esta obra os haya gustado tanto como a mí")


movimiento.rest()