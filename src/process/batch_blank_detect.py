import os
import time

import torchaudio
import torch

from paths import DATASET_DIR
import pandas as pd

v_input_dir = DATASET_DIR / "split_by_beat" / "vocals"
a_input_dir = DATASET_DIR / "split_by_beat" / "accompaniment"

csv_output_dir = DATASET_DIR / "blank_detect_beat.csv"

v_files = [f for f in os.listdir(v_input_dir)]


def detect_blank_music(path, threshold=0.008):
    try:
        y, sr = torchaudio.load(path)
        blank = int(torch.count_nonzero(torch.abs(y) < threshold))
        avg = blank / y.shape[1]
        return avg

    except:
        print("skip")
        return -1


start_time = time.time()

data = {"music_name": [], "vocals_blank": [], "accompaniment_blank": []}

for filename in v_files:
    v_path = os.path.join(v_input_dir, filename)
    a_path = os.path.join(a_input_dir, filename)

    v_blank = detect_blank_music(v_path)
    a_blank = detect_blank_music(v_path)

    if v_blank != -1 and a_blank != -1:
        data["music_name"].append(filename.split(".")[0])

        data["vocals_blank"].append(v_blank)
        data["accompaniment_blank"].append(a_blank)

    if len(data["music_name"]) % 10 == 0:
        print(len(data["music_name"]))


end_time = time.time()
print("It costs " + str(end_time - start_time) + " s")

df = pd.DataFrame(data)
df.to_csv(csv_output_dir)
