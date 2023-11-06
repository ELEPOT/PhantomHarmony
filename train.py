import os
import sys
import subprocess
import wget

DATA_DIR = 'D:/data'

validation_images = [f'{DATA_DIR}/tests/{filename}' for filename in os.listdir(f'{DATA_DIR}/tests')]
validation_prompts = [os.path.basename(img_path).split('.')[0] for img_path in validation_images]

command = []

command += ['accelerate', 'launch', f'diffusers/examples/controlnet/train_controlnet.py']
command += [
    f'--pretrained_model_name_or_path=runwayml/stable-diffusion-v1-5',

    f'--train_data_dir={DATA_DIR}/dataset/fill50k',

    f'--output_dir={DATA_DIR}/models',
    f'--cache_dir={DATA_DIR}/cache',
    f'--logging_dir={DATA_DIR}/logs',

    f'--resolution=512',
    f'--learning_rate=1e-5',
    '--train_batch_size=4',
]

command += [f'--validation_image'] + validation_images + [f'--validation_prompt'] + validation_prompts

subprocess.call(command)
