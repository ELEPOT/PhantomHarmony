import os
import subprocess

from paths import DATASET_DIR, TEST_DIR, CACHE_DIR, OUTPUT_DIR, DEPENDENCIES_DIR, VENVS_DIR

validation_dir = TEST_DIR / "no_beat_mark"

validation_images = [validation_dir / filename for filename in os.listdir(validation_dir)]
validation_prompts = [os.path.basename(img_path).split(".")[0] for img_path in validation_images]


run_name = "1_pep=0.1"

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
    "--resume_from_checkpoint=latest",
    "--resolution=512",
    "--learning_rate=1e-5",
    "--train_batch_size=4",
    "--num_validation_images=1",
    "--mixed_precision=fp16",
    "--proportion_empty_prompts=0.1",
]

command += ["--validation_image"] + validation_images + ["--validation_prompt"] + validation_prompts

subprocess.call(command)
