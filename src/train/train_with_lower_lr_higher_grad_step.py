import os
import subprocess

from paths import DATASET_DIR, VALIDATION_DIR, CACHE_DIR, OUTPUT_DIR, DEPENDENCIES_DIR, VENVS_DIR

validation_images = [VALIDATION_DIR / filename for filename in os.listdir(VALIDATION_DIR)]
validation_prompts = [os.path.basename(img_path).split(".")[0] for img_path in validation_images]

run_name = "lr2.56e-3_gas256"

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
    "--checkpointing_steps=5",
    "--validation_steps=1",
    f"--resume_from_checkpoint=latest",
    f"--resolution=512",
    f"--learning_rate=1e-3",
    "--train_batch_size=4",
    "--gradient_accumulation_steps=100",
    "--num_validation_images=1",
    "--mixed_precision=fp16",
    "--proportion_empty_prompts=0.5",
]

command += [f"--validation_image"] + validation_images + [f"--validation_prompt"] + validation_prompts

subprocess.call(command)
