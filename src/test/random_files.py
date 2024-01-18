from paths import DATA_DIR, TEST_OUTPUT_DIR
import random
import os
import shutil

input_dir = os.path.join(DATA_DIR, "dataset", "split_by_time", "accompaniment")
output_dir = os.path.join(TEST_OUTPUT_DIR, "split_by_time", "accompaniment")
files = os.listdir(input_dir)

os.makedirs(output_dir, exist_ok=True)

selected_files = random.choices(files, k=50)

for f in selected_files:
    path = os.path.join(input_dir, f)

    shutil.copy(path, output_dir)
