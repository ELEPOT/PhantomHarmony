from paths import DATASET_DIR
from generate_prompts import generate_prompt

import pandas as pd

from sklearn.utils import shuffle

max_number_of_samples_per_genre = 20

blank_detect = pd.read_csv(DATASET_DIR / "split_by_time_blank_detect.csv")
blank_detect = shuffle(blank_detect)

spotify_114k = pd.read_csv(DATASET_DIR / "spotify_114k.csv")

exclude = pd.read_csv(DATASET_DIR / "split_by_time_sample.csv")

sampled_music = []
sampled_genres = []
sampled_tags = []

for index, row in blank_detect.iterrows():
    if len(sampled_music) >= max_number_of_samples_per_genre * 111:
        break

    if row["vocals_blank"] > 0.3 or row["accompaniment_blank"] > 0.7:
        continue

    music = row["music_name"]

    if music in exclude.loc[:, "music_name"].to_list():
        continue

    genres = generate_prompt(music, include_tags=False).split()

    tags = ""
    for genre in genres:
        if sampled_genres.count(genre) >= max_number_of_samples_per_genre:
            continue

        if tags == "":
            tags = generate_prompt(music)

        sampled_music.append(music)
        sampled_genres.append(genre)
        sampled_tags.append(tags)

        print(music, genre, tags, len(sampled_music))

df = pd.DataFrame()
df["music_name"] = sampled_music
df["genre"] = sampled_genres
df["tags"] = sampled_tags

df.to_csv(DATASET_DIR / "_validation_sample_2220.csv")
