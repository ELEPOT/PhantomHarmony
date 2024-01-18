import os
import time

import torchaudio
import torch

from paths import DATA_DIR
import pandas as pd

v_input_dir = os.path.join(DATA_DIR, "dataset", "split_by_time", "vocals")
a_input_dir = os.path.join(DATA_DIR, "dataset", "split_by_time", "accompaniment")

v_files = [f for f in os.listdir(v_input_dir)]


def detect_blank_music(path, threshold=0.008):
    y, sr = torchaudio.load(path)
    blank = int(torch.count_nonzero(torch.abs(y) < threshold))
    avg = blank / y.shape[1]

    return avg


start_time = time.time()

data = {"music_name": [], "vocals_blank": [], "accompaniment_blank": []}

for filename in v_files:
    v_path = os.path.join(v_input_dir, filename)
    a_path = os.path.join(a_input_dir, filename)

    data["music_name"].append(filename.split(".")[0])
    data["vocals_blank"].append(detect_blank_music(v_path))
    data["accompaniment_blank"].append(detect_blank_music(a_path))

    if len(data["music_name"]) % 10 == 0:
        print(len(data["music_name"]))


end_time = time.time()
print("It costs " + str(end_time - start_time) + " s")

df = pd.DataFrame(data)
df.to_csv(os.path.join(DATA_DIR, "dataset", "blank_detect.csv"))
