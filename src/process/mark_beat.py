from paths import DATASET_DIR
import pandas as pd
import librosa
from PIL import Image
import numpy as np
import os

split_by_time_sample = pd.read_csv(DATASET_DIR / "split_by_time_sample.csv")

os.makedirs(DATASET_DIR / "spectrogram" / "vocals_beat_mark", exist_ok=True)

split_by_time_sample = split_by_time_sample[20]

for i, row in split_by_time_sample.iterrows():
    music_name = row["music_name"]

    output_path = DATASET_DIR / "spectrogram" / "vocals_beat_mark" / f"{music_name}.png"

    if os.path.isfile(output_path):
        if i % 100 == 0:
            print(i)
        continue

    print(music_name)

    y, sr = librosa.load(DATASET_DIR / "split_by_time" / "accompaniment" / f"{music_name}.mp3")
    img = np.array(Image.open(DATASET_DIR / "spectrogram" / "vocals" / f"{music_name}.png"))
    img[:, :, 0] = 0

    try:
        _, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_timestamps = librosa.frames_to_time(beat_frames)
        beat_cols = beat_timestamps // 0.01

        for beat_col in beat_cols:
            beat_col = int(beat_col)
            img[:, beat_col, 0] = 255

    except ValueError:
        print(f"failed to find beat of {music_name}")

    Image.fromarray(img).save(output_path)
