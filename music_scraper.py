from datasets import load_dataset
import subprocess
import os
from config import DATA_DIR

link_src: str = 'maharshipandya/spotify-tracks-dataset'
track_name_col: str = 'track_name'
artists_col: str = 'artists'
track_id_col: str = 'track_id'
output_dir: str = f'{DATA_DIR}/dataset/spotify_114k'
shuffle: bool = True
start_index: int = 0
end_index: int = -1
ban_genre: list[str] = ['classical', 'jazz', 'piano', 'sleep', 'study']


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


def track_already_downloaded(track_id):
    return os.path.exists(os.path.join(output_dir, track_id + ".mp3"))


for row in dataset:
    track_name = row[track_name_col]
    artists = row[artists_col]
    track_id = row[track_id_col]

    command = [
        "ytmdl",
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

    if track_already_downloaded(track_id):
        print(f"Skipping {track_id}")
        continue

    if artists is None or track_name is None:
        print("Skipping files with no track_name or artist info")
        continue

    subprocess.call(command)

    if track_already_downloaded(track_id):
        continue

    print("Failed. Trying not use artist info...")

    # Remove artists requirement
    command.pop(7)
    command.pop(8)

    if track_already_downloaded(track_id):
        continue

    print("Cannot find song")
