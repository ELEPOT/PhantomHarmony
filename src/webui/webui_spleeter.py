import csv
import os

from spleeter.audio import Codec
from spleeter.separator import Separator

from paths import DATASET_DIR, VENV_BIN_DIR

import subprocess


def separate_to_file(input_path, output_path):
    subprocess.call(( "spleeter", "separate", input_path, "-o", output_path))
