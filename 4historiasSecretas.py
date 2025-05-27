# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#Librerías
from naoqi import ALProxy
import time, random

# Configuración
ip = "192.168.190.85"
puerto = 9559

# Inicializar proxies
seLevanta = ALProxy("ALMotion", ip, puerto)
movimiento = ALProxy("ALRobotPosture", ip, puerto)
habla = ALProxy("ALAnimatedSpeech", ip, puerto)
tts = ALProxy("ALTextToSpeech", ip, puerto)
postura = ALProxy("ALRobotPosture", ip, puerto)
vida = ALProxy("ALAutonomousLife", ip, puerto)
vida.setState("disabled")
tts.setLanguage("Spanish")


modo_voz = True
try:
    reconocedor = ALProxy("ALSpeechRecognition", ip, puerto)
    memoria = ALProxy("ALMemory", ip, puerto)
except RuntimeError:
    print(">>> ALSpeechRecognition no disponible.")
    habla.say("El reconocimiento de voz no está disponible. ")
    modo_voz = False

#Introducción de la actividad.
movimiento.wakeUp()
movimiento.setFallManagerEnabled(True)

habla.say("Para poder entender el significado del cuadro, se me ha ocurrido una cosa. Cada grupo puede crear una historia" \
"según lo que crea que está pasando en el cuadro. ¿Qué os parece?")
habla.say("Os dejaré 10 minutos para que podáis crear vuestras historias. Pasado el tiempo, el portavoz del grupo tendrá que contarsela al resto de la clase.")

time.sleep(2)

habla.say("Es el momento de que creéis vuestras historias. Tiempo!")


seLevanta.setStiffnesses("Body", 1.0)
postura.goToPosture("Sit", 0.8)

time.sleep(600) ###Esperar 10 minutos
raw_input("Pulsa ENTER cuando pasen los 10 minutos")

habla.say("TIEMPO!!")


seLevanta.setStiffnesses("Body", 1.0)
postura.goToPosture("StandInit", 0.8)

habla.say("Es hora de escuchar vuestras historias")

grupos = ["Grupo A", "Grupo B", "Grupo C", "Grupo D"]
frases = ["Qué original", "Me encanta", "Muy bien", "Así se hace" ]

for grupo in grupos:
    habla.say("Turno del " + grupo)
    habla.say("¿Cuál es vuestra historia?")

    raw_input("Pulsa Enter para que el robot continúe...")

    habla.say(random.choice(frases))



time.sleep(5)

habla.say("Vuestras historias son maravillosas, y gracias a ellas creo que ya recuerdo el verdadero significado del cuadro." \
"¿Qué os parece si lo reconstruimos entre todos?")

habla.say("En la plaza mayor de un ajetreado pueblo del año 1559 se está librando una batalla. ¿Quiénes son los dos bandos?")
raw_input("Pulsa Enter para que el robot continúe...")
habla.say("Fenomenal")
time.sleep(2)

habla.say("A la izquierda está el grupo de Don Carnal. Van disfrazados, y llevan instrumentos, comida, bebida y muchas ganas de pasarlo bien. ¿Qué simboliza el grupo de Don Carnal?")
raw_input("Pulsa Enter para que el robot continúe...")
habla.say("Muy bien")
time.sleep(2)

habla.say("A la derecha está el grupo de Doña Cuaresma. Va acompañada por monjas y frailes que llevan pescado y otros símbolos religiosos. ¿Qué representa este grupo?")
raw_input("Pulsa Enter para que el robot continúe...")
habla.say("Así se hace")
time.sleep(2)

habla.say("Esta batalla no es de verdad, sino que es simbólica. Esto quiere decir que los bandos no están luchando de verdad, no llevan espadas ni se están haciendo daño. ¿Creéis que ellos quieren luchar de verdad?")
raw_input("Pulsa Enter para que el robot continúe...")
habla.say("Ahí va la última")
time.sleep(2)

habla.say("Mientras estos bandos se enfrentan, el pueblo, que representa la vida cotidiana, no parece prestar atención al combate. Todos llevan su vida con normalidad. Hay gente comprando, hablando, trabajando... ¿Qué creéis que puede significar esto?")
raw_input("Pulsa Enter para que el robot continúe...")

time.sleep(2)

habla.say("Ahora lo recuerdo todo! Lo que Pieter el Viejo quiere decirnos con este cuadro es que, en realidad, Don Carnal y Doña Cuaresma no solo son dos personajes, sino que representan dos maneras de vivir presentes en nuestro día a día." \
"Todos nosotros, cada día, decidimos si queremos divertirnos como Don Carnal, o si es el moemnto de cumplir con nuestras obligaciones como Doña Cuaresma. Ninguna de las dos formas de vida es buena ni mala, y ambas pueden compaginarse perfectamente, como" \
"hace el pueblo, donde hay personas que combinan la alegría con la responsabilidad. Nadie vive todos los días como Don Carnal ni como doña Cuaresma, pero todos tenemos momentos en los que somos Don Carnal, y momentos en los que somos Doña Cuaresma")
time.sleep(2)
habla.say("Lo que realmente nos quiere decir el autor con esta obra es que hay momentos para todo en la vida. Tenemos que reír, disfrutar, pasarlo bien y pasar tiempo con nuestros amigos haciendo aquellas cosas que disfrutamos, pero también" \
"debemos tener tiempo para pensar, hacer aquellas tareas que nos resultan más aburridas o que no queremos hacer, pero que hay que hacer porque serán buenas para nuestro futuro.")

movimiento.rest()