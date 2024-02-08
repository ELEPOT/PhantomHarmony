from paths import DATASET_DIR
import os

import pandas as pd

from sklearn.utils import shuffle

number_of_samples = 25

blank_detect = pd.read_csv(DATASET_DIR / "blank_detect.csv")
blank_detect = shuffle(blank_detect)
exclude = pd.read_csv(DATASET_DIR / "split_by_time_sample.csv")

sampled_music = []

for index, row in blank_detect.iterrows():
    if len(sampled_music) >= number_of_samples:
        break

    if row["music_name"] in exclude.loc[:, "music_name"].to_list():
        continue

    if row["vocals_blank"] < 0.3 and row["accompaniment_blank"] < 0.7:
        sampled_music.append(row["music_name"])

df = pd.DataFrame()
df["music_name"] = sampled_music
df.to_csv(DATASET_DIR / "validation_sample.csv")
