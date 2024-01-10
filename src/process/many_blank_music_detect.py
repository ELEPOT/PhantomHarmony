import os

import librosa
import numpy as np

from paths import TEST_OUTPUT_DIR
import pandas as pd

input_dir = os.path.join(TEST_OUTPUT_DIR,"split_by_beat","fiction")

df = pd.DataFrame()

files = [f for f in os.listdir(input_dir)]
folder_file_counts = {r:len([r+'/'+files for files in f]) for r,d,f in os.walk(input_dir)}
files_count=folder_file_counts['/home/pi/PhantomHarmony/test_output/split_by_beat/fiction']

blank_per=[]

def detect_blank_music(path):
    y, sr = librosa.load(path, sr=None)

    blank = np.count_nonzero(np.abs(y)<0.001)
    avg = blank / len(y) * 100

    return avg

for i in range(folder_file_counts['/home/pi/PhantomHarmony/test_output/split_by_beat/fiction']):
    per=detect_blank_music(os.path.join(input_dir, files[i]))
    blank_per.append(per)

df['music_name'] = files
df['blank_pertentage'] = blank_per

df.to_csv(os.path.join(TEST_OUTPUT_DIR,"test.csv"))

