import csv
import os

from spleeter.audio import Codec
from spleeter.separator import Separator

from paths import DATASET_DIR

separator = Separator("spleeter:2stems")

with open(DATASET_DIR / "spotify_114k.csv") as f:
    reader = csv.DictReader(f)

    for row in reader:
        input_path = DATASET_DIR / "spotify_114k" / row["track_id"] + ".mp3"

        if not os.path.exists(DATASET_DIR / "spleeter" / row["track_id"]):
            separator.separate_to_file(input_path, DATASET_DIR / "spleeter", codec=Codec.MP3)
