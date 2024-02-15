from paths import DATASET_DIR
import os

import pandas as pd

from sklearn.utils import shuffle

N = 4

n_of_segments_sampled_for_each_song = dict()

blank_detect = pd.read_csv(DATASET_DIR / "blank_detect_beat.csv")
blank_detect = shuffle(blank_detect)

sampled_music = []

for index, row in blank_detect.iterrows():
    name = row["music_name"].split("_")[0]

    if name in n_of_segments_sampled_for_each_song.keys():
        if n_of_segments_sampled_for_each_song[name] >= N:
            continue

    if row["vocals_blank"] < 0.3 and row["accompaniment_blank"] < 0.7:
        if name in n_of_segments_sampled_for_each_song.keys():
            n_of_segments_sampled_for_each_song[name] += 1
        else:
            n_of_segments_sampled_for_each_song[name] = 1

        sampled_music.append(row["music_name"])

df = pd.DataFrame()
df["music_name"] = sampled_music
df.to_csv(DATASET_DIR / "split_by_beat_sample.csv")
