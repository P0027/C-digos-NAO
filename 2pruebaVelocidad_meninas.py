# -*- coding: utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from naoqi import ALProxy
import time, csv, random

#Configuración
ip="192.168.174.85"
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

habla.say("El cuadro que veremos hoy será Las Meninas. " \
"Mi ayudante os lo va a mostrar en la pizarra.")
time.sleep(6)
habla.say("Este cuadro fue pintado en el año 1656, por Velázquez")
habla.say("Si os soy sincero, uno de mis sueños es ir a ver todos sus cuadros en directo, " \
"pero para llegar a Madrid hay que coger el AVE, y no creo que pueda pasar por el detector de metales.")
time.sleep(2)
habla.say("Por desgracia, no recuerdo muy bien el significado del cuadro, pero para eso estamos hoy aquí.")
habla.say("¿Qué os parece si intentamos recordarlo todos juntos?")
habla.say("Para ello, vamos a comenzar con la prueba de velocidad. Paula os va a enseñar el cuadro " \
"durante dos minutos, y tenéis que observarlo detenidamente.")
habla.say("Una vez pasado el tiempo, os haré algunas preguntas.")
time.sleep(5)
habla.say("Podéis acercaros a la pizarra para ver mejor el cuadro")
time.sleep(2)
raw_input("Pulsa enter para continuar cuando los niños estén bien colocados")

#Inicio del tiempo de observación del cuadro
habla.say("Chicos, ¿estáis preparados? Genial, entonces... Tres, dos, uno... ¡YA!")
time.sleep(2)
postura.goToPosture("Sit", 1.0)

time.sleep(120)
raw_input("Pulsa ENTER cuando hayan pasado los dos minutos") 

postura.goToPosture("StandInit", 1.0)
time.sleep(2)
habla.say("¡TIEMPO!")

#Inicio ronda de preguntas
habla.say("Ahora os voy a hacer unas preguntas. Recordad: Tenéis que levantar la mano para responder.")
habla.say("Además, la respuesta tiene que ser una única palabra. Después de deciros la pregunta, " \
"os dejaré 15 segundos para que penséis y levantéis la mano, y Paula señalará a alguien que tenga la mano levantada, " \
"quien debe responder alto y claro.")
habla.say("Recordad que no oigo muy bien, así que alto y claro!")

# Vocabulario y preguntas
vocabulario = ["nueve", "once", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "diez",
            "doce", "casa", "palacio", "habitación", "posando", "mirando", "ignorando", "pintando", "leyendo"]

preguntas = [
    "Primera pregunta: ¿Cuántas personas veis en el cuadro?",
    "Parece que todos los personajes van muy bien vestidos ¿Dónde creéis que están los personajes?",
    "Al mirar el cuadro, lo primero que vemos es una niña rubia. Ella es la infanta Margarita. ¿Qué creéis que está haciendo la infanta? ¿Creéis que está mirando a alguien, que está posando...?",
    "A la izquierda hay un hombre vestido de negro. Parece que lleva lago en la mano. ¿Qué está haciendo?"
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
                # Asegurar limpieza del motor de reconocimiento
                reconocedor.pause(True)

                # Intentar desuscribirse de cualquier subscripción previa
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

habla.say("Parece que el cuadro representa una escena familiar. En ella, hay 3 niñas, la infanta y sus ayudantes, que están en el centro de la imagen." \
"A su alrededor hay varias personas. Algunas las miran, otros están haciendo otras cosas. ¿Qué estará pasando?")
time.sleep(2)
habla.say("Para descubrirlo, vamos con la siguiente actividad")
movimiento.rest()
