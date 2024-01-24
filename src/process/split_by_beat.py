import os
import time

import soundfile as sf

from paths import EXAMPLE_DIR, TEST_OUTPUT_DIR

import torchaudio
import torch

import librosa
# parameters
input_dir = os.path.join(TEST_OUTPUT_DIR,"split_by_beat","fiction")

beat_per_section = 8

start_time = time.time()

# create output direction
vocals_output_dir = os.path.join(TEST_OUTPUT_DIR, "split_by_beat", "vocals")
accompaniment_output_dir = os.path.join(
    TEST_OUTPUT_DIR, "split_by_beat", "accompaniment"
)

os.makedirs(vocals_output_dir, exist_ok=True)
def beat():

    y, sr = torchaudio.load(path)

    channels = 2 if (y.ndim == 2 and y.shape[1] == 2) else 1

    # detect frames of beat and change frames to samples
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    # beat_frames  = np.insert(beat_frames, 0, 0)
    beat_samples = librosa.frames_to_samples(beat_frames)

    # split the vocals file, accompaniment file by section and save to output directory

    for idx in range(beat_per_section, len(beat_samples), beat_per_section):
        beat_sample_start = beat_samples[idx - beat_per_section]
        beat_sample_end = beat_samples[idx]
        sf.write(
            os.path.join(vocals_output_dir, "%s_%05d.mp3" % int(idx / beat_per_section)),
            v_y[beat_sample_start:beat_sample_end],
            sr,
            format="mp3",
        )

        sf.write(
            os.path.join(vocals_output_dir, "%05d.mp3" % int(idx / beat_per_section)),
            y[beat_sample_start:beat_sample_end],
            sr,
            format="mp3",
        )


    print("Finsh parsing %s in %d seconds." % (original_path, (time.time() - start_time)))
