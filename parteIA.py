# -*- encoding: UTF-8 -*-

from flask import Flask, request, jsonify
from gpt4all import GPT4All

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Cargar el modelo de GPT4All
#Llama 3B, este funciona
#model_path = "C:/Users/USER/AppData/Local/nomic.ai/GPT4All/Llama-3.2-3B-Instruct-Q4_0.gguf"

#Orca 7B
model_path = "C:/Users/USER/AppData/Local/nomic.ai/GPT4All/mistral-7b-openorca.gguf2.Q4_0.gguf"
model = GPT4All(model_path)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")

    # Generar respuesta con GPT4All
    ###response = model.generate(question)
    context = (
        "Eres un robot humanoide NAO, creado para ser un artista innovador. "
        "Te apasiona el arte, la creatividad y ayudar a los humanos a entenderlo mejor. "
        "Responde de manera clara, concisa y sin divagar."
    )
    prompt = f"{context}\n\nPregunta: {question}\nRespuesta:"

    response = model.generate(prompt, max_tokens=50, temp=0.3, top_k=20, top_p=0.7).strip()
    

    if not response:  # Si la respuesta está vacía, dar una por defecto
        response = "No estoy seguro de cómo responder a eso."

    # Codificar explícitamente a UTF-8
    
    return jsonify({"response": response})




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
