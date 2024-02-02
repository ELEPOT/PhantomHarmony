from diffusers import StableDiffusionControlNetPipeline ,ControlNetModel
import torch
import cv2
img = cv2.imread('/home/leo/blues.png')

controlnet_model_path = "/mnt/d/models/diffusion_pytorch_model.safetensors"
#main_model_path = "/mnt/d/models/riffusion-model-v1.safetensors"
#url = "https://huggingface.co/leo1008/test/main/diffusion_pytorch_model.safetensors"  # can also be a local path
controlnet = ControlNetModel.from_pretrained("leo1008/test", torch_dtype=torch.float16)

pipe = StableDiffusionControlNetPipeline.from_pretrained("riffusion/riffusion-model-v1", controlnet=controlnet, torch_dtype=torch.float16)

torch.manual_seed(0)
generator = torch.random.manual_seed(0)

output_path = "happy.png"

out_image = pipe(
    "guitar", num_inference_steps=20, generator=generator, image=img
).images[0]

out_image.save(output_path)
'''
error msg

Traceback (most recent call last):
  File "/home/leo/PhantomHarmony/src/process/diff.py", line 9, in <module>
    controlnet = ControlNetModel.from_pretrained("leo1008/test", torch_dtype=torch.float16)
  File "/home/leo/test/lib/python3.10/site-packages/huggingface_hub/utils/_validators.py", line 118, in _inner_fn
    return fn(*args, **kwargs)
  File "/home/leo/test/lib/python3.10/site-packages/diffusers/models/modeling_utils.py", line 669, in from_pretrained
    unexpected_keys = load_model_dict_into_meta(
  File "/home/leo/test/lib/python3.10/site-packages/diffusers/models/modeling_utils.py", line 154, in load_model_dict_into_meta
    raise ValueError(
ValueError: Cannot load leo1008/test because down_blocks.0.attentions.0.transformer_blocks.0.attn2.to_k.weight expected shape tensor(..., device='meta', size=(320, 1280)), but got torch.Size([320, 768]). If you want to instead overwrite randomly initialized weights, please make sure to pass both `low_cpu_mem_usage=False` and `ignore_mismatched_sizes=True`. For more information, see also: https://github.com/huggingface/diffusers/issues/1619#issuecomment-1345604389 as an example.
'''
