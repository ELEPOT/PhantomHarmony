import os
import subprocess

from config import DATA_DIR, DEPENDENCIES_DIR

validation_images = [
    f"{DATA_DIR}/tests/{filename}" for filename in os.listdir(f"{DATA_DIR}/tests")
]
validation_prompts = [
    os.path.basename(img_path).split(".")[0] for img_path in validation_images
]

command = []

command += [
    "accelerate",
    "launch",
    os.path.join(DEPENDENCIES_DIR, "diffusers/examples/controlnet/train_controlnet.py"),
]

command += [
    f"--pretrained_model_name_or_path=riffusion/riffusion-model-v1",
    f"--train_data_dir={DATA_DIR}/dataset/spectrograms",
    f"--output_dir={DATA_DIR}/models",
    f"--cache_dir={DATA_DIR}/cache",
    f"--logging_dir={DATA_DIR}/logs",
    f"--resolution=512",
    f"--learning_rate=1e-5",
    "--train_batch_size=4",
]

command += (
    [f"--validation_image"]
    + validation_images
    + [f"--validation_prompt"]
    + validation_prompts
)

subprocess.call(command)
