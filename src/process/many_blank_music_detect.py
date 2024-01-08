import os

import librosa
import numpy as np

from paths import TEST_OUTPUT_DIR

input_dir = os.path.join(TEST_OUTPUT_DIR,"split_by_beat","fiction")


def detect_blank_music(path):
    print(path)
    y, sr = librosa.load(path, sr=None)

    # print(len(y))
    blank = np.count_nonzero(np.abs(y)<0.001)
    # print(blank)
    avg = blank / len(y) * 100

    return avg

folder_file_counts = {r:len([r+'/'+files for files in f]) for r,d,f in os.walk(input_dir)}
#folder_file_counts=int(folder_file_counts)
print(folder_file_counts)
for i in range(folder_file_counts['/home/pi/PhantomHarmony/test_output/split_by_beat/fiction']):
    print(detect_blank_music(os.path.join(input_dir, "%05d" % (i+1)+".mp3")))
#print(detect_blank_music(os.path.join(input_dir, "00001.mp3")))
#print(detect_blank_music(os.path.join(input_dir, "00016.mp3")))
