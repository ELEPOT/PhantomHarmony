from paths import DATASET_DIR, TEST_OUTPUT_DIR
import random
import os
import shutil

input_dir = DATASET_DIR / "dataset" / "split_by_time" / "accompaniment"
output_dir = TEST_OUTPUT_DIR / "split_by_time" / "accompaniment"
files = os.listdir(input_dir)

os.makedirs(output_dir, exist_ok=True)

selected_files = random.choices(files, k=50)

for f in selected_files:
    path = input_dir / f

    shutil.copy(path, output_dir)
