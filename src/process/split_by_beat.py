import os
import time
from pathlib import Path

from paths import DATASET_DIR
import torchaudio
import librosa
import pandas as pd

# parameters
input_dir = DATASET_DIR / "spleeter"
out_dir = DATASET_DIR / "split_by_beat"

beat_per_section = 8

start_time = time.time()


def beat(beat_path, vocals_path, accompaniment_path, out_path):
    track_id = Path(beat_path).stem

    if os.path.exists(out_path / "vocals" / f"{track_id}_00001.mp3"):
        return

    y, sr = torchaudio.load(beat_path)
    v_y, sr = torchaudio.load(vocals_path)
    a_y, sr = torchaudio.load(accompaniment_path)

    # detect frames of beat and change frames to samples
    _, beat_frames = librosa.beat.beat_track(y=y.numpy()[0], sr=sr)

    # beat_frames  = np.insert(beat_frames, 0, 0)
    beat_samples = librosa.frames_to_samples(beat_frames)

    # split the vocals file, accompaniment file by section and save to output directory

    os.makedirs(out_path / "vocals", exist_ok=True)
    os.makedirs(out_path / "accompaniment", exist_ok=True)

    for idx in range(beat_per_section, len(beat_samples), beat_per_section):
        beat_sample_start = beat_samples[idx - beat_per_section]
        beat_sample_end = beat_samples[idx]

        filename = f"{track_id}_{idx // 8 : 05d}.mp3"
        v_path = out_path / "vocals" / filename
        a_path = out_path / "accompaniment" / filename

        if not os.path.exists(v_path):
            torchaudio.save(
                v_path,
                v_y[:, beat_sample_start:beat_sample_end],
                sr,
            )

        if not os.path.exists(a_path):
            torchaudio.save(
                a_path,
                a_y[:, beat_sample_start:beat_sample_end],
                sr,
            )


for i, f in pd.read_csv(DATASET_DIR / "spotify_114k.csv").iterrows():
    f = f["track_id"]

    if i % 100 == 0:
        print(i, f)

    beat(
        DATASET_DIR / "spotify_114k" / (f + ".mp3"),
        input_dir / f / "vocals.mp3",
        input_dir / f / "accompaniment.mp3",
        out_dir,
    )

print("Finsh parsing %s in %d seconds." % (input_dir, (time.time() - start_time)))
