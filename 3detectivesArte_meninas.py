# -*- encoding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import csv, time
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
    habla.say("El reconocimiento de voz no está disponible.")
    modo_voz = False



# Vocabulario de reconocimiento
vocabulario = ["Velazquez", "pintor", "artista", "nadie", "padre", "amigo", "hermano", "padres", "madre", "reyes"
               "familiares", "desconocidos", "mascota", "colado", "nosotros", "alguien más", "alguien", "sí", "no"]

preguntas = [
    "El hombre de la izquierda parece pintar algo. Su cara me resulta familiar... ¿Quién puede ser? ¿Algún conocido de la familia, un pintor de renombre?",
    "En el fondo de la obra, en el espejo, hay reflejadas dos personas. ¿Quiénes pueden ser? ¿Serán familiares o desconocidos?",
    "Hay un perro en la escena. ¿Creéis que es la mascota de las niñas, o que se ha colado?",
    "Hay un hombre en la puerta de la sala. ¿A quién creéis que mira? ¿A nosotros? ¿O hay alguien más en esa sala?"
]

grupos = ["Grupo A", "Grupo B"]

# Crear archivo CSV
with open(archivoRespuestas, mode="w") as f:
    writer = csv.writer(f)
    writer.writerow(["Pregunta", "Grupo", "Respuesta grupo", "Tiempo de respuesta (s)"])

# --- ACTIVIDAD PRINCIPAL ---
for ronda, pregunta in enumerate(preguntas):
    habla.say("Ronda " + str(ronda + 1) + ". Atención detectives: " + pregunta)
    print("\n" + pregunta)
    habla.say("¡Empieza el tiempo de pensar!")
    
    
    raw_input("Pulsa ENTER cuando pasen 3 mins")


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

habla.say("Parece que ya hemos descubierto algunas cosas interesantes." \
" En el centro del cuadro vemos a la infanta Margarita, una niña muy importante. A su lado están sus damas de honor, las meninas, que " \
"la cuidan y la acompañan. Un poco más atrás, vemos al pintor… ¡es Velázquez! Él mismo se ha pintado mientras trabaja. En el fondo, alguien " \
"entra por una puerta. Y si miramos bien el espejo… aparecen los reyes, que son los padres de la infanta. Tal vez están delante, mirando la escena." \
" O tal vez… nos están mirando a nosotros. Nadie sonríe mucho, pero todo parece muy tranquilo, como si todos supieran que algo importante está pasando.")


habla.say("Ahora ya sabemos lo que está pasando en el cuadro pero, aún queda lo más importante... ¿Qué querría el autor decirnos con esto?")

#Poner código de pensar

habla.say("Para descubrirlo, vamos con la última actividad. ¡Lo estáis haciendo genial!")

print("Actividad completada. Resultados guardados en:", archivoRespuestas)
