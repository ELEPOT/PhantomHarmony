import csv
import os

from spleeter.audio import Codec
from spleeter.separator import Separator

from config import DATA_DIR

separator = Separator("spleeter:2stems")

with open(os.path.join(DATA_DIR, "dataset", "spotify_114k.csv")) as f:
    reader = csv.DictReader(f)

    for row in reader:
        path = os.path.join(DATA_DIR, "dataset", "spotify_114k", row["track_id"] + ".mp3")
        out_path = os.path.join(DATA_DIR, "dataset", "spleeter")

        if not os.path.exists(os.path.join(out_path, row["track_id"])):
            separator.separate_to_file(path, out_path, codec=Codec.MP3)
