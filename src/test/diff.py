from paths import NEXTCLOUD_MODEL_DIR, NEXTCLOUD_RIFFUSION_DIR

from diffusers import *
from transformers import *
from diffusers.schedulers import PNDMScheduler
from diffusers.pipelines.stable_diffusion.safety_checker import StableDiffusionSafetyChecker
import torch
from PIL import Image
import os

torch.set_default_device("cuda")


def load_model(root_model_dir=None, use_controlnet=True):
    #torch.set_default_device("cuda")

    if root_model_dir != None and os.path.isdir(root_model_dir / "unet"):
        print("using self unet")
        main_model_path = root_model_dir / "unet"
    else:
        main_model_path = NEXTCLOUD_RIFFUSION_DIR / "unet"

    main_model = UNet2DConditionModel.from_pretrained(main_model_path)
    vae = AutoencoderKL.from_pretrained(NEXTCLOUD_RIFFUSION_DIR / "vae")
    text_encoder = CLIPTextModel.from_pretrained(NEXTCLOUD_RIFFUSION_DIR / "text_encoder")
    tokenizer = CLIPTokenizer.from_pretrained(NEXTCLOUD_RIFFUSION_DIR / "tokenizer")
    scheduler = PNDMScheduler.from_pretrained(NEXTCLOUD_RIFFUSION_DIR / "scheduler")
    safety_checker = StableDiffusionSafetyChecker.from_pretrained(NEXTCLOUD_RIFFUSION_DIR / "safety_checker")
    feature_extractor = CLIPImageProcessor.from_pretrained(NEXTCLOUD_RIFFUSION_DIR / "feature_extractor")

    if use_controlnet:
        controlnet_model_path = root_model_dir / "controlnet"
        controlnet = ControlNetModel.from_pretrained(controlnet_model_path)

        pipe = StableDiffusionControlNetPipeline(
            vae, text_encoder, tokenizer, main_model, controlnet, scheduler, safety_checker, feature_extractor
        ).to("cuda")

    else:
        pipe = StableDiffusionPipeline(
            vae, text_encoder, tokenizer, main_model, scheduler, safety_checker, feature_extractor
        ).to("cuda")

    return pipe


def run_pipeline(pipe, input_path, output_path, text, times):
    torch.manual_seed(0)
    generator = torch.random.manual_seed(0)

    if isinstance(pipe, StableDiffusionControlNetPipeline):
        img = Image.open(input_path)
        img = img.crop((0, 0, 512, 512))

        out_image = pipe(text, num_inference_steps=times, generator=generator, image=img).images[0]

    else:
        out_image = pipe(text, num_inference_steps=20, generator=generator).images[0]

    out_image.save(output_path)
