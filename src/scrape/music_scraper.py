import csv
import os
import subprocess

from datasets import load_dataset

from paths import DATASET_DIR, VENV_BIN_DIR

link_src: str = "maharshipandya/spotify-tracks-dataset"
output_dir: str = DATASET_DIR / "spotify_114k"
shuffle: bool = True
start_index: int = 0
end_index: int = -1
exclude_genre: list[str] = ["classical", "sleep", "study"]
min_duration_ms = 2 * 60 * 1000
max_duration_ms = 7 * 60 * 1000

if not os.path.isdir(output_dir):
    os.makedirs(output_dir, exist_ok=True)

dataset = load_dataset(link_src, split="train")

if shuffle:
    dataset = dataset.shuffle(seed=4242)

dataset = dataset.to_list()

if end_index == -1:
    dataset = dataset[start_index:]
else:
    dataset = dataset[start_index:end_index]


def track_already_downloaded(_track_id):
    return os.path.exists(os.path.join(output_dir, _track_id + ".mp3"))


def add_track_to_final_dataset(_track_id):
    if _track_id not in final_dataset.keys():
        final_dataset[_track_id] = row
    elif final_dataset[_track_id]["track_genre"] != row["track_genre"]:
        final_dataset[_track_id]["track_genre"] += "," + row["track_genre"]


"""
    final_dataset = {
        track_id_0: {"track_id": track_id_0, "track_name": ... }, 
        track_id_1: {"track_id": track_id_1, "track_name": ... }, 
        ...
    }
"""

final_dataset = {}

for row in dataset:
    track_name = row["track_name"]
    artists = row["artists"]
    track_id = row["track_id"]

    if artists is None or track_name is None:
        # print("Skipping files with no track_name or artist info")
        continue

    if (
        row["track_genre"] in exclude_genre
        or not min_duration_ms < row["duration_ms"] < max_duration_ms
        or row["instrumentalness"] > 0.1
    ):
        # print(f"Excluding {track_id}")
        continue

    if track_already_downloaded(track_id):
        # print(f"Skipping {track_id}")
        add_track_to_final_dataset(track_id)
        continue

    command = [
        os.path.join(VENV_BIN_DIR, "ytmdl"),
        track_name,
        "-q",
        "--skip-meta",
        "--ignore-errors",
        "--on-meta-error",
        "skip",
        "--artist",
        artists,
        "-o",
        f"{output_dir}",
        "--filename",
        track_id,
        "--nolocal",
        "--dont-transcode",
    ]

    subprocess.call(command)

    if track_already_downloaded(track_id):
        add_track_to_final_dataset(track_id)
        continue

    print("Failed. Trying not using artist info...")

    # Remove artists requirement
    command.pop(7)
    command.pop(7)

    subprocess.call(command)

    if track_already_downloaded(track_id):
        add_track_to_final_dataset(track_id)
        continue

    print("Cannot find song, skipping...")

with open(DATASET_DIR / "spotify_114k.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=dataset[0].keys())
    writer.writeheader()
    writer.writerows(final_dataset.values())
