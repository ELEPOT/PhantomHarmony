import pandas as pd
import os
from paths import DATASET_DIR

samples = pd.read_csv(DATASET_DIR / "split_by_time_sample.csv")
spotify_114k = pd.read_csv(DATASET_DIR / "spotify_114k.csv")

vocals_paths = []
accompaniment_paths = []
prompt = []

for index, sample in samples.iterrows():
    vocals_paths.append(os.path.join("vocals", sample["music_name"] + ".png"))
    accompaniment_paths.append(os.path.join("accompaniment", sample["music_name"] + ".png"))
    prompt.append(
        spotify_114k.loc[spotify_114k["track_id"] == sample["music_name"].split("_")[0]].iloc[0]["track_genre"]
    )

    if index % 100 == 0:
        print(index)


df = pd.DataFrame()
df["text"] = prompt
df["image"] = accompaniment_paths
df["conditioning_image"] = vocals_paths

df.to_json(DATASET_DIR / "spectrogram" / "train.jsonl", orient="records", lines=True)
