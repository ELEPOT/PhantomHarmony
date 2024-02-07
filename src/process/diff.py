from paths import NEXTCLOUD_MODEL_DIR

from diffusers import *
from transformers import *
from diffusers.schedulers import PNDMScheduler
from diffusers.pipelines.stable_diffusion.safety_checker import StableDiffusionSafetyChecker
import torch
from PIL import Image

controlnet_model_path = NEXTCLOUD_MODEL_DIR / "first-7500/controlnet"
main_model_path = NEXTCLOUD_MODEL_DIR / "riffusion/unet"

controlnet = ControlNetModel.from_pretrained(controlnet_model_path)
main_model = UNet2DConditionModel.from_pretrained(main_model_path)
vae = AutoencoderKL.from_pretrained(NEXTCLOUD_MODEL_DIR / "riffusion/vae")
text_encoder = CLIPTextModel.from_pretrained(NEXTCLOUD_MODEL_DIR / "riffusion/text_encoder")
tokenizer = CLIPTokenizer.from_pretrained(NEXTCLOUD_MODEL_DIR / "riffusion/tokenizer")
scheduler = PNDMScheduler.from_pretrained(NEXTCLOUD_MODEL_DIR / "riffusion/scheduler")
safety_checker = StableDiffusionSafetyChecker.from_pretrained(NEXTCLOUD_MODEL_DIR / "riffusion/safety_checker")
feature_extractor = CLIPImageProcessor.from_pretrained(NEXTCLOUD_MODEL_DIR / "riffusion/feature_extractor")

pipe = StableDiffusionControlNetPipeline(
    vae, text_encoder, tokenizer, main_model, controlnet, scheduler, safety_checker, feature_extractor
).to("cuda")


def diff(output_path, input_path, magic_code):
    torch.set_default_device("cuda")

    img = Image.open(input_path)

    torch.manual_seed(0)
    generator = torch.random.manual_seed(0)

    out_image = pipe(magic_code, num_inference_steps=20, generator=generator, image=img).images[0]

    out_image.save(output_path)
