from paths import DATASET_DIR
import os

import pandas as pd

from sklearn.utils import shuffle

number_of_samples_per_genre = 20

blank_detect = pd.read_csv(DATASET_DIR / "split_by_time_blank_detect.csv")
spotify_114k = pd.read_csv(DATASET_DIR / "spotify_114k.csv")
blank_detect = shuffle(blank_detect)
exclude = pd.read_csv(DATASET_DIR / "split_by_time_sample.csv")

sampled_music = []
sampled_genres = []

for index, row in blank_detect.iterrows():
    # print(len(sampled_music))
    if len(sampled_music) >= number_of_samples_per_genre * 111:
        break

    music = row["music_name"]

    if music in exclude.loc[:, "music_name"].to_list():
        continue

    # print(music)
    genre = spotify_114k.loc[spotify_114k["track_id"] == music.split("_")[0]].iloc[0]["track_genre"]

    # Just ignore if there are more than one genre to one track
    # They're too complicated
    if "," in genre:
        continue

    if sampled_genres.count(genre) >= number_of_samples_per_genre:
        # print("skip")
        continue

    else:
        print(genre)

    if row["vocals_blank"] < 0.3 and row["accompaniment_blank"] < 0.7:
        sampled_music.append(music)
        sampled_genres.append(genre)

df = pd.DataFrame()
df["music_name"] = sampled_music
df["genre"] = sampled_genres

df.to_csv(DATASET_DIR / "validation_sample_2220.csv")
