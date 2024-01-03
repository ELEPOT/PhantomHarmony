import os

import librosa
import numpy as np

from paths import EXAMPLE_DIR

y, sr = librosa.load(os.path.join(EXAMPLE_DIR, "fiction.mp3"), sr=None)

print(len(y))
blank = np.count_nonzero(y == 0)

print(blank)
avg = blank / len(y) * 100
print(avg)
