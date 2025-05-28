from diffusers import StableDiffusionPipeline
import torch

# Cargar el modelo
pipe = StableDiffusionPipeline.from_pretrained(
    "lykon/dreamshaper-8",
    torch_dtype=torch.float32,
    safety_checker = None
)

pipe = pipe.to("cuda")

# Prompt
prompt = "A kid in front of a castle, during winter, where he is dancing with a girl , concept art, digital painting, trending on artstation, fantasy style, colorful, cartoon"

cuadro = pipe(prompt, num_inference_steps=25).images[0]

cuadro.save("imagen_generada3.png")
