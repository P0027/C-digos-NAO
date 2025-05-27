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
seLevanta = ALProxy("ALMotion", ip, puerto)
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
    print(">>> ALSpeechRecognition no disponible. Se usará entrada por teclado.")
    habla.say("El reconocimiento de voz no está disponible. Se usará el teclado.")
    modo_voz = False

#Introducción de la actividad.
movimiento.wakeUp()
movimiento.setFallManagerEnabled(True)

habla.say("Vamos genial, chicos! Se me ocurre que ahora podemos estudiar el cuadro en mayor profundidad... ¿Qué os parece si nos fijamos aún más en los detalles?")
time.sleep(2)
habla.say("Muy bien! Para que esta actividad sea más sencilla, vamos a dividirnos en cuatro grupos y elegir un portavoz de cada grupo.")
habla.say("Tenéis dos minutos para dividiros, que empiezan ya!")

time.sleep(120)   ###AQUÍ VAN LOS DOS MINUTOS
raw_input("Pulsa ENTER cuando estén divididos")

habla.say("Ahora que estáis divididos, os explicaré el juego. Os haré una pregunta, la misma para todos los grupos. Tendréis 3 minutos para observar el cuadro" \
"y debatir la respuesta. Una vez que la tengáis, preguntaré grupo por grupo vuestra respuesta." \
"¿Qué os parece?")
time.sleep(1)
habla.say("Recordad, todas las respuestas son válidas, así que no la cambiéis a última hora!")
time.sleep(2)
habla.say("Chicos, ¿estáis preparados?")
time.sleep(2)
habla.say("¡Genial!, ¡Comencemos!")


# Vocabulario de reconocimiento
vocabulario = ["comida", "carne", "queso", "bebida", "instrumentos", "flauta", "espadas", "zambomba", "guitarra", "alcohol"
               "tambores", "disfraces", "tristes", "contentos", "alterados", "enfadados", "neutrales", "impasibles", "indiferentes", "animados",
               "nerviosos", "cruz", "simbolo religioso", "pan", "pescado", "serios", "ignorándolos", "prestando atención", "les importa", "mirando", "interesados"]

preguntas = [
    "¿Qué llevan los personajes de la izquierda en las manos?",
    "¿Qué actitud tienen los personajes de la izquierda? ¿Están contentos, tristes...?",
    "¿Qué llevan los personajes de la derecha en las manos?",
    "¿Qué actitud tienen los personajes de la derecha? ¿Están tristes, contentos...?",
    "¿Qué actitud tienen las personas que están en el fondo del cuadro? ¿Parecen interesados en la batalla, o están ignorándolos?"
]

grupos = ["Grupo A", "Grupo B", "Grupo C", "Grupo D"]

# Crear archivo CSV
with open(archivoRespuestas, mode="w") as f:
    writer = csv.writer(f)
    writer.writerow(["Pregunta", "Grupo", "Respuesta grupo", "Tiempo de respuesta (s)"])

# --- ACTIVIDAD PRINCIPAL ---
for ronda, pregunta in enumerate(preguntas):
    habla.say("Ronda " + str(ronda + 1) + ". Atención detectives: " + pregunta)
    print("\n" + pregunta)
    habla.say("¡Empieza el tiempo de pensar!")
    
    postura.goToPosture("Sit", 1.0)

    time.sleep(180)  ###AQUÍ VAN LOS TRES MINUTOS
    raw_input("Pulsa ENTER cuando estén preparados")

    seLevanta.setStiffnesses("Body", 1.0)
    postura.goToPosture("StandInit", 1.0)

    habla.say("¡TIEMPO! Hora de responder")

    for grupo in grupos:
        habla.say("Turno del " + grupo)
        print("\n[" + grupo + "]")

        inicio = time.time()

        if modo_voz:
            # Preparar reconocimiento
            try:
                escucha.pause(True)
                escucha.unsubscribe("EscuchaTemp")
                time.sleep(0.3)
            except:
                pass

            try:
                memoria.insertData("WordRecognized", [])
            except:
                pass

            escucha.setLanguage("Spanish")
            escucha.setVocabulary(vocabulario, False)
            time.sleep(0.3)

            nombre_suscripcion = "Escucha_{}_Ronda{}".format(grupo.replace(" ", "_"), ronda)
            escucha.subscribe(nombre_suscripcion)
            time.sleep(0.3)
            escucha.pause(False)

            print("Escuchando respuesta hablada...")
            palabraReconocida = None
            tiempoInicio = time.time()

            while time.time() - tiempoInicio < 8:
                try:
                    datos = memoria.getData("WordRecognized")
                    if isinstance(datos, list) and len(datos) >= 2 and datos[1] > 0.35:
                        palabraReconocida = datos[0]
                        break
                except:
                    pass
                time.sleep(0.2)

            try:
                escucha.unsubscribe(nombre_suscripcion)
            except RuntimeError as e:
                if "non-subscribed" not in str(e):
                    print(">>> Error al desuscribir:", e)

            if palabraReconocida:
                respuestaGrupo = palabraReconocida
                print("→ Reconocido:", respuestaGrupo)
            else:
                respuestaGrupo = raw_input("Respuesta no escuchada. Respuesta del grupo: ")
                
                

        else:
            respuestaGrupo = raw_input("Respuesta del grupo: ")

        tiempoRespuesta = round(time.time() - inicio, 2)
        print("Tiempo:", tiempoRespuesta, "s")

        # Guardar en CSV
        with open(archivoRespuestas, mode="a") as f:
            writer = csv.writer(f)
            writer.writerow([pregunta, grupo, respuestaGrupo, tiempoRespuesta])

    habla.say("Fin de la ronda " + str(ronda + 1) + ". Vamos a la siguiente.")

habla.say("¡Felicidades detectives! Habéis respondido todas las preguntas genial, y gracias a vosotros vuelvo a recordar algo...")

habla.say("En el pueblo se está librando una batalla. Don Carnal es el rey del carnaval, y le encanta comer, beber, salir de fiesta y pasárselo bien.Las personas que lo rodean llevan disfraces, tocan instrumentos, comen y beben. Este grupo representa la fiesta, pasárselo bien e ignorar las resposabilidades y las consecuencias. Por otra parte, " \
"Doña Cuaresma es una anciana tranquila y seria. Va en un carrito tirado por monjas, y las personas que la acompañan llevan en sus manos símbolos religiosos y van con la cabeza agachada, en señal de obediencia. Ellos representan la espiritualidad, el autocontrol y la responsabilidad, justo al contrario que Don Carnal.  Nadie va ganando ni perdiendo, y el pueblo, representado" \
"en la parte central del cuadro, ignora completamente la batalla.")

habla.say("Ahora ya sabemos lo que está pasando en el cuadro pero, aún queda lo más importante... ¿Qué querría el autor decirnos con esto?")


habla.say("Para descubrirlo, vamos con la última actividad. ¡Lo estáis haciendo genial!")

print("Actividad completada. Resultados guardados en:", archivoRespuestas)
