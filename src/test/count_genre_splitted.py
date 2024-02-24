from paths import DATASET_DIR
import pandas as pd
from pprint import pprint

blank_detect = pd.read_csv(DATASET_DIR / "split_by_time_sample.csv")
spotify_114k = pd.read_csv(DATASET_DIR / "spotify_114k.csv")

genre_count = {}

for index, row in blank_detect.iterrows():
    music = row["music_name"]
    genres = spotify_114k.loc[spotify_114k["track_id"] == music.split("_")[0]].iloc[0]["track_genre"].split(",")

    print(genres)
    for genre in genres:
        if genre in genre_count.keys():
            genre_count[genre] += 1
        else:
            genre_count[genre] = 1


genre_count = list(genre_count.items())

genre_count.sort(key=lambda x: x[1], reverse=True)

pprint(genre_count)
