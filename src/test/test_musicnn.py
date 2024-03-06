import pandas as pd
from paths import DATASET_DIR, TEST_OUTPUT_DIR, DEPENDENCIES_DIR
import sys

sys.path.append(str(DEPENDENCIES_DIR / "musicnn"))

from musicnn.extractor import extractor
import numpy as np


samples = pd.read_csv(DATASET_DIR / "split_by_time_sample.csv")
spotify_114k = pd.read_csv(DATASET_DIR / "spotify_114k.csv")

valid_tags = [
    "guitar",
    "techno",
    "electronic",
    "rock",
    "piano",
    "ambient",
    "indian",
    "opera",
    "dance",
    "country",
    "new age",
    "metal",
]

occur_sum = np.zeros((len(valid_tags), len(valid_tags)))
occur_len = np.zeros_like(occur_sum)

for i, sample in samples.iterrows():
    sample = sample["music_name"]

    try:
        genres = spotify_114k.loc[spotify_114k["track_id"] == sample.split("_")[0]].iloc[0]["track_genre"].split(",")
    except:
        print(sample)

    if occur_len.all() >= 100:
        break

    for genre_i, genre in enumerate(valid_tags):
        if genre == "new age":
            genre = "new-age"
        if genre in genres:
            if (occur_len[genre_i] < 100).any():
                taggram, tags = extractor(
                    DATASET_DIR / "split_by_time" / "accompaniment" / f"{sample}.mp3", extract_features=False
                )
                tags_likelihood_mean = np.mean(taggram, axis=0)

                tags_likelihood_mean = dict(zip(tags, tags_likelihood_mean))

                for tag_i, tag in enumerate(valid_tags):
                    occur_sum[genre_i, tag_i] += tags_likelihood_mean[tag]

                occur_len[genre_i] += 1

    if i % 10 == 0:
        print(occur_sum / occur_len)

print(occur_sum / occur_len)

with open(TEST_OUTPUT_DIR / "test_musicnn.npy", "wb") as f:
    np.save(f, occur_sum / occur_len)
