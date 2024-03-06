import pandas as pd
import os
from paths import DATASET_DIR
from musicnn.tagger import top_tags
from random import gauss, randint
import numpy as np

samples = pd.read_csv(DATASET_DIR / "split_by_time_sample.csv")
spotify_114k = pd.read_csv(DATASET_DIR / "spotify_114k.csv")

vocals_paths = []
vocals_beat_mark_paths = []
accompaniment_paths = []
prompts = []


def shuffle_slightly(x, orderliness=0.5):
    x = sorted(enumerate(x), key=lambda i: gauss(i[0] * orderliness, 1))
    return list(dict(x).values())


for i, sample in samples.iterrows():
    sample = sample["music_name"]

    vocals_paths.append(os.path.join("vocals", sample + ".png"))
    accompaniment_paths.append(os.path.join("accompaniment", sample + ".png"))
    vocals_beat_mark_paths.append(os.path.join("vocals_beat_mark", sample + ".png"))

    prompt = spotify_114k.loc[spotify_114k["track_id"] == sample.split("_")[0]].iloc[0]["track_genre"].split(",")
    prompt += top_tags(str(DATASET_DIR / "split_by_time" / "accompaniment" / f"{sample}.mp3"), topN=10)
    prompt = shuffle_slightly(prompt)
    prompt = prompt[: randint(1, 11)]
    prompt = " ".join(prompt)

    prompts.append(prompt)

    print(prompt)


df = pd.DataFrame()
df["text"] = prompts
df["image"] = accompaniment_paths
df["conditioning_image"] = vocals_paths
df["conditioning_image_with_beat_mark"] = vocals_beat_mark_paths

df.to_json(DATASET_DIR / "spectrogram" / "train.jsonl", orient="records", lines=True)
