import os
import time

import librosa
import soundfile as sf

# parameters
filename = "fiction.mp3"
beat_per_section = 8

start_time = time.time()

# create output direction
output_dir = os.path.join(".", "split_into_section", os.path.splitext(filename)[0])
os.makedirs(output_dir, exist_ok=True)

# load file
#   `sr`: sampling rate of the file
#   `channel`: channel of the file
y, sr = librosa.load(filename, sr=None)  # according to document of librosa,
# `sr` should assigned to None to preserve the native sampling rate of the file
channels = 2 if (y.ndim == 2 and y.shape[1] == 2) else 1

# detect frames of beat and change frames to samples
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
# beat_frames  = np.insert(beat_frames, 0, 0)
beat_samples = librosa.frames_to_samples(beat_frames)

# split the file by section and save to output direction
for idx in range(beat_per_section, len(beat_samples), beat_per_section):
    beat_sample_start = beat_samples[idx - beat_per_section]
    beat_sample_end = beat_samples[idx]
    sf.write(
        os.path.join(output_dir, "%05d.mp3" % int(idx / beat_per_section)),
        y[beat_sample_start:beat_sample_end],
        sr,
        format="mp3",
    )

print("Finsh parsing %s in %d seconds." % (filename, (time.time() - start_time)))
