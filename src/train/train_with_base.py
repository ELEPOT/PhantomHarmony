import os
import subprocess

from paths import DATASET_DIR, VALIDATION_DIR, CACHE_DIR, OUTPUT_DIR, DEPENDENCIES_DIR, VENVS_DIR

validation_images = [VALIDATION_DIR / filename for filename in os.listdir(VALIDATION_DIR)]
validation_prompts = [os.path.basename(img_path).split(".")[0] for img_path in validation_images]

run_name = "train_base"

command = []

command += [
    VENVS_DIR / "dev" / "bin" / "python",
    os.path.join(DEPENDENCIES_DIR, "diffusers/examples/controlnet/train_controlnet.py"),
]

command += [
    "--pretrained_model_name_or_path=riffusion/riffusion-model-v1",
    f"--train_data_dir={DATASET_DIR}/spectrogram",
    f"--output_dir={OUTPUT_DIR}/{run_name}/models",
    f"--cache_dir={CACHE_DIR}",
    f"--logging_dir={OUTPUT_DIR}/{run_name}",
    "--report_to=wandb",
    f"--resume_from_checkpoint=latest",
    f"--resolution=512",
    f"--learning_rate=1e-5",  # Lower lr (suggested by official `train.md`)
    "--train_batch_size=2",  # My computer cannot handle such batch size with train_base :(
    "--num_validation_images=1",
    "--gradient_accumulation_steps=2",  # To stay consistent
    "--mixed_precision=fp16",
    "--train_base",
]

command += [f"--validation_image"] + validation_images + [f"--validation_prompt"] + validation_prompts

subprocess.call(command)
