from diffusers import StableDiffusionPipeline
import torch

# Cargar el modelo usando precisión float16 para GPU
pipe = StableDiffusionPipeline.from_pretrained(
    "lykon/dreamshaper-8",  # o el que uses
    torch_dtype=torch.float32,
    safety_checker = None
)

# Enviar el modelo a la GPU (si la tienes activada)
pipe = pipe.to("cuda")

# Prompt para probar
prompt = "A mad kid in front of a island, during summer, where he is dancing with a cat , concept art, digital painting, trending on artstation, fantasy style, colorful, cartoon"

# Puedes reducir el número de pasos para acelerar aún más (opcional)
image = pipe(prompt, num_inference_steps=25).images[0]

# Guardar la imagen
image.save("imagen_generada3.png")
