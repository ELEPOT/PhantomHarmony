import os
import subprocess

from paths import DATA_DIR, DEPENDENCIES_DIR, VENV_BIN_DIR, VENV_PYTHON_DIR

validation_images = [f"{DATA_DIR}/tests/{filename}" for filename in os.listdir(f"{DATA_DIR}/tests")]
validation_prompts = [os.path.basename(img_path).split(".")[0] for img_path in validation_images]

command = []

command += [
    VENV_PYTHON_DIR,
    os.path.join(DEPENDENCIES_DIR, "diffusers/examples/controlnet/train_controlnet.py"),
]

command += [
    f"--pretrained_model_name_or_path=riffusion/riffusion-model-v1",
    f"--train_data_dir={DATA_DIR}/dataset/spectrogram",
    f"--output_dir=/mnt/e/output/fp16_lr1e-5_train_base/models/",
    f"--cache_dir={DATA_DIR}/cache",
    f"--logging_dir=/mnt/e/output/fp16_lr1e-5_train_base",
    f"--resume_from_checkpoint=latest",
    f"--resolution=512",
    f"--learning_rate=2e-6",  # Lower lr (suggested by official `train.md`)
    "--train_batch_size=2",  # My computer cannot handle such batch size with train_base :(
    "--gradient_accumulation_steps=2",  # To stay consistent
    "--num_validation_images=1",
    "--mixed_precision=fp16",
    "--proportion_empty_prompts=0.5",
    "--train_base",
]

command += [f"--validation_image"] + validation_images + [f"--validation_prompt"] + validation_prompts

subprocess.call(command)
