import csv
import os

from spleeter.audio import Codec
from spleeter.separator import Separator

from paths import DATASET_DIR

separator = Separator("spleeter:2stems")
def separate_to_file(input_path ,output_path)
    separator.separate_to_file(input_path, output_path, codec=Codec.MP3)