import os

from paths import DATASET_DIR

from src.riffusion.spectrogram_params import SpectrogramParams
from src.riffusion.spectrogram_image_converter import SpectrogramImageConverter

import csv
from pydub import AudioSegment

params = SpectrogramParams()
converter = SpectrogramImageConverter(params)

v_input_dir = DATASET_DIR / "split_by_time" / "vocals"
a_input_dir = DATASET_DIR / "split_by_time" / "accompaniment"

v_spec_output_dir = DATASET_DIR / "spectrogram" / "vocals"
a_spec_output_dir = DATASET_DIR / "spectrogram" / "accompaniment"

split_sampled_csv_dir = DATASET_DIR / "split_by_time_sample.csv"


os.makedirs(v_spec_output_dir, exist_ok=True)
os.makedirs(a_spec_output_dir, exist_ok=True)

with open(split_sampled_csv_dir) as f:
    reader = csv.DictReader(f)

    for row in reader:
        v_path = v_input_dir / (row["music_name"] + ".mp3")
        a_path = a_input_dir / (row["music_name"] + ".mp3")

        v_out_path = v_spec_output_dir / (row["music_name"] + ".png")
        a_out_path = v_spec_output_dir / (row["music_name"] + ".png")

        converter.spectrogram_image_from_audio(AudioSegment.from_mp3(v_path)).save(v_out_path)
        converter.spectrogram_image_from_audio(AudioSegment.from_mp3(a_path)).save(a_out_path)
