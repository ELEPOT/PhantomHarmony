from paths import NEXTCLOUD_MODEL_DIR

from diffusers import *
from transformers import *
from diffusers.schedulers import PNDMScheduler
from diffusers.pipelines.stable_diffusion.safety_checker import StableDiffusionSafetyChecker
import torch
from PIL import Image
import os

torch.set_default_device("cuda")


def load_model(root_model_dir):
    torch.set_default_device("cuda")
    controlnet_model_path = root_model_dir / "controlnet"

    if os.path.isdir(root_model_dir / "unet"):
        main_model_path = root_model_dir / "unet"
    else:
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

    return pipe


def run_pipeline(pipe, input_path, output_path, text):
    img = Image.open(input_path)

    torch.manual_seed(0)
    generator = torch.random.manual_seed(0)

    out_image = pipe(text, num_inference_steps=20, generator=generator, image=img).images[0]

    out_image.save(output_path)
