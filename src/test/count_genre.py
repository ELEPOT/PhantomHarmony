import csv
import os
from pprint import pprint

from paths import DATASET_DIR

genre_count = {}

with open(DATASET_DIR / "spotify_114k.csv", "r") as f:
    reader = csv.DictReader(f)

    for row in reader:
        genres = row["track_genre"].split(",")
        for genre in genres:
            if genre in genre_count.keys():
                genre_count[genre] += 1
            else:
                genre_count[genre] = 1

genre_count = list(genre_count.items())

genre_count.sort(key=lambda x: x[1], reverse=True)

pprint(genre_count)
