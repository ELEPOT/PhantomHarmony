from paths import DATASET_DIR
import os

import pandas as pd

from sklearn.utils import shuffle

max_number_of_samples_per_song = 4

number_of_samples_per_song = dict()

blank_detect = pd.read_csv(DATASET_DIR / "blank_detect_beat.csv")
blank_detect = shuffle(blank_detect)

sampled_music = []

for index, row in blank_detect.iterrows():
    name = row["music_name"].split("_")[0]

    if name in number_of_samples_per_song.keys():
        if number_of_samples_per_song[name] >= max_number_of_samples_per_song:
            continue

    if row["vocals_blank"] < 0.3 and row["accompaniment_blank"] < 0.7:
        if name in number_of_samples_per_song.keys():
            number_of_samples_per_song[name] += 1
        else:
            number_of_samples_per_song[name] = 1

        sampled_music.append(row["music_name"])

df = pd.DataFrame()
df["music_name"] = sampled_music
df.to_csv(DATASET_DIR / "split_by_beat_sample.csv")
