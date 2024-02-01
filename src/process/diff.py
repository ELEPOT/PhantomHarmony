'''from diffusers import StableDiffusionPipeline
#from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
import torch
pipeline = StableDiffusionPipeline.from_single_file(
    "/mnt/f/models/dreamshaper_8.safetensors"
)
pipeline.to("cuda")
image = pipeline("An image of a squirrel in Picasso style").images[0]
image.save("image_of_squirrel_painting.png")
'''
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
import torch
import cv2
img = cv2.imread('blues.png')
controlnet = ControlNetModel.from_single_file(
    "/mnt/d/models/diffusion_pytorch_model.safetensors", torch_dtype=torch.float16)

pipe = StableDiffusionControlNetPipeline.from_single_file(
    "/mnt/d/models/riffusion-model-v1.ckpt", controlnet=controlnet, torch_dtype=torch.float16
)
generator = torch.manual_seed(0)

out_image = pipe(
    "guitar", num_inference_steps=20, generator=generator, image=img
).images[0]
image.save("happy.png")
