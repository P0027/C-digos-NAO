# -*- coding: utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from naoqi import ALProxy
import time, csv, random

#Configuración
ip="192.168.190.85"
puerto=9559

# Proxies
movimiento = ALProxy("ALMotion", ip, puerto)
postura = ALProxy("ALRobotPosture", ip, puerto)
texto = ALProxy("ALTextToSpeech", ip, puerto)
habla = ALProxy("ALAnimatedSpeech", ip, puerto)
texto.setLanguage("Spanish")

# Intentar inicializar reconocimiento de voz
modo_voz = True
try:
    reconocedor = ALProxy("ALSpeechRecognition", ip, puerto)
    memoria = ALProxy("ALMemory", ip, puerto)
except RuntimeError:
    print("ALSpeechRecognition no disponible.")
    modo_voz = False

# Introducción de la actividad
movimiento.wakeUp()
movimiento.setFallManagerEnabled(True)

habla.say("El cuadro que veremos hoy será La batalla entre Don Carnal y Doña Cuaresma. " \
"Mi ayudante os lo va a mostrar en la pizarra.")
time.sleep(6)
habla.say("Este cuadro fue pintado en el año 1559, por el pintor Pieter Brueghel, apodado El Viejo.")
habla.say("Si os soy sincero, uno de mis sueños es ir a ver todos sus cuadros en directo, " \
"pero están en Viena, y no creo que pueda pasar por el detector de metales del aeropuerto.")
time.sleep(2)
habla.say("Por desgracia, no recuerdo muy bien el significado del cuadro, pero para eso estamos hoy aquí.")
habla.say("¿Qué os parece si intentamos recordarlo todos juntos?")
habla.say("Para ello, vamos a comenzar con la prueba de velocidad. Paula os va a enseñar el cuadro " \
"durante dos minutos, y tenéis que observarlo detenidamente.")
habla.say("Una vez pasado el tiempo, os haré algunas preguntas.")
time.sleep(5)
habla.say("Podéis acercaros a la pizarra para ver el cuadro mejor")
time.sleep(2)
raw_input("Pulsa enter para continuar cuando los niños estén bien colocados")

#Inicio del tiempo de observación del cuadro
habla.say("Chicos, ¿estáis preparados? Genial, entonces... Tres, dos, uno... ¡YA!")
postura.goToPosture("Sit", 1.0)

time.sleep(120) 
raw_input("Pulsa ENTER cuando estén listos")

postura.goToPosture("StandInit", 1.0)
habla.say("¡TIEMPO!")

#Inicio ronda de preguntas
habla.say("Ahora os voy a hacer unas preguntas. Recordad: Tenéis que levantar la mano para responder.")
habla.say("Además, la respuesta tiene que ser una única palabra. Después de deciros la pregunta, " \
"os dejaré 15 segundos para que penséis y levantéis la mano, y Paula señalará a alguien que tenga la mano levantada, " \
"quien debe responder alto y claro.")
habla.say("Recordad que no oigo muy bien, así que alto y claro!")

# Vocabulario y preguntas
vocabulario = ["pueblo", "plaza", "campo", "calle", "parque", "aldea", "arriba", "abajo", "centro", "derecha", "izquierda",
            "todos igual de importantes", "unos más importantes que otros", "mujer", "vieja", "hombre", "gordo", "no hay", "si hay"]

preguntas = [
    "Primera pregunta: ¿Dónde ocurre esta escena? En un pueblo, en el campo, en una plaza...",
    "Hay gente haciendo cosas extrañas en el cuadro pero, ¿dónde? Arriba, abajo, en medio...",
    "¿Hay personajes peleando en el cuadro? ¿Dónde? Arriba, abajo, en medio, o no hay"
]

respuestasPositivas = ["¡Genial!", "¡Muy bien!", "¡Así se hace!"]

# Guardar resultados en el CSV
with open("pruebaVelocidad_respuestas.csv", "a") as f:
    writer = csv.writer(f)
    writer.writerow(["Pregunta", "TiempoRespuesta", "Respuesta"])

    for pregunta in preguntas:
        habla.say(pregunta)
        habla.say("Tenéis 15 segundos para pensar!")
        time.sleep(15)
        habla.say("¿Cuál es vuestra respuesta?")

        inicio = time.time()

        if modo_voz:
            try:
                reconocedor.pause(True)

                for sub in ["EscuchaPregunta", "EscuchaTemp"]:
                    try:
                        reconocedor.unsubscribe(sub)
                    except RuntimeError as e:
                        if "was not subscribed" not in str(e):
                            print("Error al desuscribir", sub, ":", e)

                memoria.insertData("WordRecognized", [])
                reconocedor.setLanguage("Spanish")
                reconocedor.setVocabulary(vocabulario, False)
                time.sleep(0.3)

                reconocedor.subscribe("EscuchaPregunta")
                reconocedor.pause(False)

                print("Escuchando respuesta hablada...")

                palabraReconocida = None
                tiempoInicio = time.time()

                while time.time() - tiempoInicio < 10:
                    try:
                        datos = memoria.getData("WordRecognized")
                        if isinstance(datos, list) and len(datos) >= 2 and datos[1] > 0.35:
                            palabraReconocida = datos[0]
                            break
                    except:
                        pass
                    time.sleep(0.2)

                try:
                    reconocedor.unsubscribe("EscuchaPregunta")
                except RuntimeError as e:
                    if "non-subscribed" not in str(e):
                        print(">>> Error al desuscribir: ", e)

                if palabraReconocida:
                    respuesta = palabraReconocida
                    print("Respuesta:", respuesta)
                else:
                    habla.say("No te he entendido bien. ¿Podrías escribir tu respuesta en la pizarra?")
                    movimiento.moveTo(0.0, 0.0, 2.75) 
                    respuesta = raw_input("Respuesta no escuchada. Escribe la respuesta del niño: ")
                    habla.say("Entiendo")
                    movimiento.moveTo(0.0, 0.0, -3.0)

            except Exception as e:
                print("Error en reconocimiento de voz:", e)
                respuesta = raw_input("Tu respuesta (modo manual): ")

        else:
            respuesta = raw_input("Tu respuesta: ")

        tiempoRespuesta = round(time.time() - inicio, 2)
        print(">> Respuesta: %s | Tiempo: %.2f segundos" % (respuesta, tiempoRespuesta))
        writer.writerow([pregunta, tiempoRespuesta, respuesta])

        habla.say(random.choice(respuestasPositivas))
        time.sleep(2)

habla.say("Creo que poco a poco empiezo a recordar.")

# Brazo derecho a la cabeza
movimiento.setAngles("RShoulderPitch", 0.6 , 0.2)    
movimiento.setAngles("RShoulderRoll", 0.5, 0.2)
movimiento.setAngles("RElbowYaw", 1.4, 0.2)
movimiento.setAngles("RElbowRoll", 1.2, 0.2)
movimiento.setAngles("RWristYaw", 0.1, 0.2)
movimiento.setAngles("RHand", 1.0, 0.2)
# Giro de cabeza
movimiento.setAngles("HeadYaw", 0.4, 0.2)         
movimiento.setAngles("HeadPitch", -0.1, 0.2)
# Brazo izq en jarra
movimiento.setAngles("LShoulderPitch", 1.45, 0.2)  
movimiento.setAngles("LShoulderRoll", 0.25, 0.2)     
movimiento.setAngles("LElbowYaw", -1.0, 0.2)         
movimiento.setAngles("LElbowRoll", -1.4, 0.2)        
movimiento.setAngles("LWristYaw", -0.4, 0.2)         
movimiento.setAngles("LHand", 1.0, 0.2)

habla.say("Parece que el cuadro muestra a mucha gente en una plaza... Hay dos grupos de personajes que parece que" \
"están librando una batalla, mientras que otros simplemente siguen con sus vidas. Pero, ¿por qué están peleando los personajes?")
time.sleep(2)
habla.say("Para descubrirlo, vamos con la siguiente actividad")
movimiento.rest()
