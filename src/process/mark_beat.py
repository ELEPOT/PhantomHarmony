from paths import DATASET_DIR
import pandas as pd
import librosa
from PIL import Image
import numpy as np
import os


def mark_beat(output_spectrogram_path, input_audio_path, input_spectrogram_path):
    if os.path.isfile(output_spectrogram_path) and output_spectrogram_path != input_spectrogram_path:
        return

    y, sr = librosa.load(input_audio_path)
    img = np.array(Image.open(input_spectrogram_path))
    img[:, :, 0] = 0

    try:
        _, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_timestamps = librosa.frames_to_time(beat_frames)
        beat_cols = beat_timestamps // 0.01

        for beat_col in beat_cols:
            beat_col = int(beat_col)
            img[:, beat_col, 0] = 255

    except ValueError:
        print(f"failed to find beat of {input_audio_path}")

    Image.fromarray(img).save(output_spectrogram_path)


if __name__ == "__main__":
    split_by_time_sample = pd.read_csv(DATASET_DIR / "split_by_time_sample.csv")

    os.makedirs(DATASET_DIR / "spectrogram" / "vocals_beat_mark", exist_ok=True)
    for i, row in split_by_time_sample.iterrows():
        mark_beat(
            DATASET_DIR / "spectrogram" / "vocals_beat_mark" / f"{row['music_name']}.png",
            DATASET_DIR / "split_by_time" / "accompaniment" / f"{row['music_name']}.mp3",
            DATASET_DIR / "spectrogram" / "vocals" / f"{row['music_name']}.png",
        )
