import os

import librosa
import numpy as np

from paths import EXAMPLE_DIR

input_dir = os.path.join(EXAMPLE_DIR, "spleeter_example")


def detect_blank_music(path):
    print(path)
    y, sr = librosa.load(path, sr=None)

    # print(len(y))
    blank = np.count_nonzero(np.any(np.abs(y) < 0.01 and np.abs(y) > -0.01) )
    # print(blank)
    avg = blank / len(y) * 100

    return avg


print(detect_blank_music(os.path.join(EXAMPLE_DIR, "vocals_full.mp3")))
print(detect_blank_music(os.path.join(EXAMPLE_DIR, "vocals_blank.mp3")))
