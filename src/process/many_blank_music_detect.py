import os

import librosa
import numpy as np

from paths import TEST_OUTPUT_DIR
import pandas as pd
input_dir = os.path.join(TEST_OUTPUT_DIR,"split_by_beat","fiction")
df = pd.DataFrame()
files = [f for f in os.listdir(input_dir)]
print(files)
folder_file_counts = {r:len([r+'/'+files for files in f]) for r,d,f in os.walk(input_dir)}
files_count=folder_file_counts['/home/pi/PhantomHarmony/test_output/split_by_beat/fiction']
blank_per=[]

def detect_blank_music(path):
    #print(path)
    y, sr = librosa.load(path, sr=None)

    # print(len(y))
    blank = np.count_nonzero(np.abs(y)<0.001)
    # print(blank)
    avg = blank / len(y) * 100

    return avg

#folder_file_counts = {r:len([r+'/'+files for files in f]) for r,d,f in os.walk(input_dir)}
#folder_file_counts=int(folder_file_counts)
#print(folder_file_counts)
for i in range(folder_file_counts['/home/pi/PhantomHarmony/test_output/split_by_beat/fiction']):
    per=detect_blank_music(os.path.join(input_dir, files[i]))
    blank_per.append(per)
print(blank_per)
#print(detect_blank_music(os.path.join(input_dir, "00001.mp3")))
#print(detect_blank_music(os.path.join(input_dir, "00016.mp3")))
df['music_name'] = files
df['blank_pertentage'] = blank_per
df.to_csv("test.csv")
