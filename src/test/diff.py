from paths import NEXTCLOUD_MODEL_DIR, NEXTCLOUD_RIFFUSION_DIR

from diffusers import *
from transformers import *
from diffusers.schedulers import PNDMScheduler
from diffusers.pipelines.stable_diffusion.safety_checker import StableDiffusionSafetyChecker
import torch
from PIL import Image
import os

torch.set_default_device("cuda")


def load_model(root_model_dir=None):
    # torch.set_default_device("cuda")

    if root_model_dir != None and os.path.isdir(root_model_dir / "unet"):
        print("using self unet")
        main_model_path = root_model_dir / "unet"
    else:
        main_model_path = NEXTCLOUD_RIFFUSION_DIR / "unet"

    controlnet_model_path = root_model_dir / "controlnet"

    main_model = UNet2DConditionModel.from_pretrained(main_model_path)
    vae = AutoencoderKL.from_pretrained(NEXTCLOUD_RIFFUSION_DIR / "vae")
    text_encoder = CLIPTextModel.from_pretrained(NEXTCLOUD_RIFFUSION_DIR / "text_encoder")
    tokenizer = CLIPTokenizer.from_pretrained(NEXTCLOUD_RIFFUSION_DIR / "tokenizer")
    scheduler = PNDMScheduler.from_pretrained(NEXTCLOUD_RIFFUSION_DIR / "scheduler")
    safety_checker = None
    feature_extractor = CLIPImageProcessor.from_pretrained(NEXTCLOUD_RIFFUSION_DIR / "feature_extractor")

    if os.path.isdir(controlnet_model_path):
        print("using controlnet")

        if os.path.isfile(controlnet_model_path / "diffusion_pytorch_model.safetensors"):
            controlnet = ControlNetModel.from_pretrained(controlnet_model_path)
        else:
            controlnet = ControlNetModel.from_single_file(str(controlnet_model_path / "diffusion_pytorch_model.ckpt"))

        pipe = StableDiffusionControlNetPipeline(
            vae,
            text_encoder,
            tokenizer,
            main_model,
            controlnet,
            scheduler,
            safety_checker,
            feature_extractor,
            requires_safety_checker=False,
        ).to("cuda")

    else:
        pipe = StableDiffusionPipeline(
            vae,
            text_encoder,
            tokenizer,
            main_model,
            scheduler,
            safety_checker,
            feature_extractor,
            requires_safety_checker=False,
        ).to("cuda")

    return pipe


def run_pipeline(pipe, input_path, output_path, text, times=20):
    torch.manual_seed(0)
    generator = torch.random.manual_seed(0)

    if isinstance(pipe, StableDiffusionControlNetPipeline):
        img = Image.open(input_path)
        img = img.crop((0, 0, 512, 512))

        out_image = pipe(text, num_inference_steps=times, generator=generator, image=img).images[0]

    else:
        out_image = pipe(text, num_inference_steps=times, generator=generator).images[0]

    out_image.save(output_path)
