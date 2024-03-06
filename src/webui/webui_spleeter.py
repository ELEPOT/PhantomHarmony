from paths import DATASET_DIR, VENVS_DIR

import subprocess


def separate_to_file(input_path, output_path):
    subprocess.call((VENVS_DIR / "webui" / "bin" / "spleeter", "separate", input_path, "-o", output_path))
