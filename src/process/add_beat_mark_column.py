import pandas as pd
import os
from paths import DATASET_DIR

input_path = pd.read_json(DATASET_DIR / "spectrogram" / "train.jsonl", orient="records", lines=True)
samples = pd.read_csv(DATASET_DIR / "split_by_time_sample.csv")

vocals_beat_mark_paths = []

for index, sample in samples.iterrows():
    vocals_beat_mark_paths.append(os.path.join("vocals_beat_mark", sample["music_name"] + ".png"))

    if index % 100 == 0:
        print(index)


input_path["conditioning_image_with_beat_mark"] = vocals_beat_mark_paths

input_path.to_json(DATASET_DIR / "spectrogram" / "train.jsonl", orient="records", lines=True)
