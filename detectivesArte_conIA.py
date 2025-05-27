# -*- encoding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests, csv, time, re
from naoqi import ALProxy

# --- CONFIGURACIÓN ---
ip = "127.0.0.1"
puerto = 9559
servidorAI = "http://127.0.0.1:5000/ask"
archivoRespuestas = "resultados_detectivesArte.csv"

# Inicializar proxies
habla = ALProxy("ALTextToSpeech", ip, puerto)
habla.setLanguage("Spanish")

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
habla.say("Gracias a vuestra ayuda, estoy empezando a recordar algunas cosas sobre el cuadro... Si no me equivoco, había una gran historia escondida tras él, pero no consigo recordar como era.")

#####Hacer como si se echa la mano a la cara y niega

habla.say("Se me ocurre que, si vemos las partes importantes")
habla.say("Vamos genial, chicos! Se me ocurre que ahora podemos estudiar el cuadro en mayor profundidad... ¿Qué os parece si nos fijamos aún más en los detalles?")
time.sleep(5)
habla.say("Muy bien! A ")



# Vocabulario de reconocimiento
vocabulario = ["personajes", "personas", "figuras", "centro", "mirando", "espectador",
               "sombrero", "rojo", "tres", "cuatro", "cinco", "veinte", "siete"]

preguntas = [
    {
        "pregunta": "¿Cuántos personajes puedes contar en la escena principal del cuadro?",
        "respuesta": "Hay más de veinte personajes, pero siete son los principales en el centro."
    },
    {
        "pregunta": "¿Qué personaje está haciendo algo diferente al resto?",
        "respuesta": "El personaje del centro está mirando hacia el espectador mientras los demás miran a los lados."
    },
    {
        "pregunta": "¿Qué objeto aparece repetido varias veces en el cuadro?",
        "respuesta": "El sombrero rojo aparece en al menos tres figuras distintas."
    }
]

grupos = ["Grupo A", "Grupo B", "Grupo C", "Grupo D"]

# Crear archivo CSV si no existe
with open(archivoRespuestas, mode="w") as f:
    archivo = csv.writer(f)
    archivo.writerow(["Pregunta", "Grupo", "Respuesta grupo", "Respuesta correcta", "Similitud (%)", "Tiempo de respuesta (s)"])

# --- Función para IA ---
def obtener_similitud(respuestaDada, respuestaCorrecta):
    prompt = u"""
Eres un evaluador de respuestas. Se te dan dos frases: una es la respuesta de un alumno, y la otra es la respuesta correcta esperada.
Tu tarea es indicar la similitud entre el contenido de ambas en una escala de 0% (nada similares) a 100% (completamente iguales en significado).
Devuelve SOLO un número entero del 0 al 100, seguido del símbolo %.

Frase del alumno: "{}"
Frase correcta: "{}"
""".format(respuestaDada, respuestaCorrecta)

    try:
        response = requests.post(servidorAI, json={"question": prompt})
        if response.status_code == 200:
            raw = response.json()["response"]
            match = re.search(r'(\d{1,3})\s*%', raw)
            if match:
                valor = int(match.group(1))
                valor = min(max(valor, 0), 100)

                if valor < 25:
                    habla.say("No exactamente...")
                elif valor < 75:
                    habla.say("¡Vais por buen camino!")
                else:
                    habla.say("¡Exacto!")
                return valor
            else:
                print(">>> No se encontró porcentaje válido en la respuesta.")
                return 0
        else:
            print(">>> Error al contactar con el servidor")
            return 0
    except Exception as e:
        print(">>> Excepción al obtener similitud:", e)
        return 0

# --- ACTIVIDAD PRINCIPAL ---
for ronda, pregunta_info in enumerate(preguntas):
    pregunta = pregunta_info["pregunta"]
    respuestaCorrecta = pregunta_info["respuesta"]

    habla.say("Ronda " + str(ronda + 1) + ". Atención detectives: " + pregunta)
    print("\n" + pregunta)

    for grupo in grupos:
        habla.say("Turno del " + grupo)
        print("\n[" + grupo + "]")

        inicio = time.time()

        if modo_voz:
            # --- Configuración del reconocimiento ---
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
            time.sleep(1.5)

            tiempoInicio = time.time()
            while time.time() - tiempoInicio < 8:
                try:
                    respuestaMemoria = memoria.getData("WordRecognized")
                    if isinstance(respuestaMemoria, list) and len(respuestaMemoria) >= 2 and respuestaMemoria[1] > 0.35:
                        palabraReconocida = respuestaMemoria[0]
                        break
                except RuntimeError:
                    pass
                time.sleep(0.2)

            try:
                escucha.unsubscribe(nombre_suscripcion)
            except RuntimeError as e:
                if "non-subscribed module" not in str(e):
                    print(">>> Error al desuscribir:", e)

            if palabraReconocida:
                respuestaGrupo = palabraReconocida
                print("→ Reconocido por voz:", respuestaGrupo)
            else:
                habla.say("No escuché nada. Por favor, escribe la respuesta.")
                respuestaGrupo = raw_input("Respuesta del grupo: ")

        else:
            respuestaGrupo = raw_input("Respuesta del grupo: ")

        fin = time.time()
        tiempoRespuesta = round(fin - inicio, 2)

        similitud = obtener_similitud(respuestaGrupo, respuestaCorrecta)

        print("Similitud:", similitud, "%")
        print("Tiempo:", tiempoRespuesta, "s")

        with open(archivoRespuestas, mode="a") as f:
            writer = csv.writer(f)
            writer.writerow([pregunta, grupo, respuestaGrupo, respuestaCorrecta, similitud, tiempoRespuesta])

    habla.say("Fin de la ronda " + str(ronda + 1) + ". Vamos a la siguiente.")

habla.say("¡Felicidades detectives! Han llegado al final del misterio.")
print("\nActividad completada. Resultados guardados en:", archivoRespuestas)
