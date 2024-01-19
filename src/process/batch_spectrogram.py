import os

from paths import DATA_DIR

from riffusion.spectrogram_params import SpectrogramParams
from riffusion.spectrogram_image_converter import SpectrogramImageConverter

import csv
from pydub import AudioSegment

params = SpectrogramParams()
converter = SpectrogramImageConverter(params)

os.makedirs(os.path.join(DATA_DIR, "dataset", "spectrogram", "vocals"), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "dataset", "spectrogram", "accompaniment"), exist_ok=True)

with open(os.path.join(DATA_DIR, "dataset", "blank_detect.csv")) as f:
    reader = csv.DictReader(f)

    for row in reader:
        v_path = os.path.join(DATA_DIR, "dataset", "split_by_time", "vocals", row["music_name"] + ".mp3")
        a_path = os.path.join(DATA_DIR, "dataset", "split_by_time", "accompaniment", row["music_name"] + ".mp3")

        v_out_path = os.path.join(DATA_DIR, "dataset", "spectrogram", "vocals", row["music_name"] + ".png")
        a_out_path = os.path.join(DATA_DIR, "dataset", "spectrogram", "accompaniment", row["music_name"] + ".png")

        converter.spectrogram_image_from_audio(AudioSegment.from_mp3(v_path)).save(v_out_path)
        converter.spectrogram_image_from_audio(AudioSegment.from_mp3(a_path)).save(a_out_path)
