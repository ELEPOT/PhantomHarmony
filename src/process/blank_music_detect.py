import os

import librosa

from paths import EXAMPLE_DIR

y, sr = librosa.load(os.path.join(EXAMPLE_DIR, "fiction.mp3"), sr=None)

blank = 0
print(len(y))
for i in range(len(y)):
    # print(y[i])
    if y[i] == 0:
        # print(y[i],i)
        blank = blank + 1
print(blank)
avg = blank / len(y) * 100
print(avg)
