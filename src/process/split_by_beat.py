import os
import time
from pathlib import Path

from paths import DATASET_DIR
import torchaudio
import librosa

# parameters
input_dir = DATASET_DIR / "spleeter"
out_dir = DATASET_DIR / "split_by_beat"

dirs = [f for f in os.listdir(input_dir)]

beat_per_section = 8

start_time = time.time()


def beat(beat_path, vocals_path, accompaniment_path, out_path):
    track_id = Path(beat_path).stem

    if os.path.exists(os.path.join(out_path, "vocals", "%s_%05d.mp3" % (track_id, 1))):
        print("skip")
        return

    y, sr = torchaudio.load(
        beat_path,
    )
    v_y, sr = torchaudio.load(vocals_path)
    a_y, sr = torchaudio.load(accompaniment_path)

    # detect frames of beat and change frames to samples
    tempo, beat_frames = librosa.beat.beat_track(y=y.numpy()[0], sr=sr)

    # beat_frames  = np.insert(beat_frames, 0, 0)
    beat_samples = librosa.frames_to_samples(beat_frames)

    # split the vocals file, accompaniment file by section and save to output directory

    os.makedirs(os.path.join(out_path, "vocals"), exist_ok=True)
    os.makedirs(os.path.join(out_path, "accompaniment"), exist_ok=True)

    for idx in range(beat_per_section, len(beat_samples), beat_per_section):
        beat_sample_start = beat_samples[idx - beat_per_section]
        beat_sample_end = beat_samples[idx]

        v_path = os.path.join(out_path, "vocals", "%s_%05d.mp3" % (track_id, idx // 8))
        a_path = os.path.join(out_path, "accompaniment", "%s_%05d.mp3" % (track_id, idx // 8))
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


for f in dirs:
    beat(
        DATASET_DIR / "spotify_114k" / f + ".mp3",
        input_dir / f / "vocals.mp3",
        input_dir / f / "accompaniment.mp3",
        out_dir,
    )

print("Finsh parsing %s in %d seconds." % (input_dir, (time.time() - start_time)))
