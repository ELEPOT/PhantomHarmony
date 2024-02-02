from diffusers import StableDiffusionControlNetPipeline ,ControlNetModel
import torch
import cv2
img = cv2.imread('/home/leo/blues.png')

controlnet_model_path = "/mnt/d/models/diffusion_pytorch_model.safetensors"
main_model_path = "/mnt/d/models/riffusion-model-v1.safetensors"

controlnet = ControlNetModel.from_single_file(controlnet_model_path, torch_dtype=torch.float16)

pipe = StableDiffusionControlNetPipeline.from_pretrained("riffusion/riffusion-model-v1", controlnet=controlnet, torch_dtype=torch.float16)

torch.manual_seed(0)
generator = torch.random.manual_seed(0)

output_path = "happy.png"

out_image = pipe(
    "guitar", num_inference_steps=20, generator=generator, image=img
).images[0]

out_image.save(output_path)
