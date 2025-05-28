# -*- encoding: UTF-8 -*-

from flask import Flask, request, jsonify
from gpt4all import GPT4All

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Cargar el modelo
ruta_modelo = "C:/Users/USER/AppData/Local/nomic.ai/GPT4All/mistral-7b-openorca.gguf2.Q4_0.gguf"
modelo = GPT4All(ruta_modelo)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    pregunta = data.get("pregunta", "")

    #Prompt
    contexto = (
        "Eres un robot humanoide NAO, creado para ser un artista. "
        "Te apasiona el arte, la creatividad y ayudar a los humanos a entenderlo mejor. "
        "Responde de manera clara, concisa y sin divagar."
    )
    prompt = f"{contexto}\n\nPregunta: {pregunta}\nRespuesta:"

    respuesta = modelo.generate(prompt, max_tokens=50, temp=0.3, top_k=20, top_p=0.7).strip()
    

    if not respuesta:
        respuesta = "No estoy seguro de cómo responder a eso."

    
    return jsonify({"Respuesta": respuesta})




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
