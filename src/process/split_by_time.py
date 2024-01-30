import librosa
import soundfile as sf

from paths import DATASET_DIR
import os
import csv

import torchaudio
import torch


def split_by_time(path, out_path, track_id, time_per_section=5.12):
    y, sr = torchaudio.load(path)

    # Convert y from stereo to mono
    y = torch.mean(y, dim=0).unsqueeze(0)[0]

    samples_per_section = int(sr * time_per_section)
    idx = 0

    os.makedirs(out_path, exist_ok=True)

    for start in range(0, y.size()[0] - samples_per_section, samples_per_section):
        end = start + samples_per_section
        sep_y = y[start:end]

        # Convert size (samples) to (1, samples)
        sep_y = sep_y.view((1, sep_y.shape[0]))

        torchaudio.save(os.path.join(out_path, "%s_%05d.mp3" % (track_id, idx)), sep_y, sr)
        idx += 1

    print("Finished splitting %s" % track_id)


with open(DATASET_DIR / "spotify_114k.csv") as f:
    reader = csv.DictReader(f)

    spleeter_dir = DATASET_DIR / "spleeter"

    for row in reader:
        split_by_time(
            path=spleeter_dir / row["track_id"] / "vocals.mp3",
            out_path=DATASET_DIR / "split_by_time" / "vocals",
            track_id=row["track_id"],
        )

        split_by_time(
            path=spleeter_dir / row["track_id"] / "accompaniment.mp3",
            out_path=DATASET_DIR / "split_by_time" / "accompaniment",
            track_id=row["track_id"],
        )
