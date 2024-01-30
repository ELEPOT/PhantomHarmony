from process.batch_blank_detect import detect_blank_music
import numpy as np
from paths import EXAMPLE_DIR, TEST_OUTPUT_DIR
import os
import csv

with open(os.path.join(TEST_OUTPUT_DIR, "threshold_test.csv"), "w") as f:
    writer = csv.writer(f)

    for threshold in np.arange(0, 0.5, 0.001):
        writer.writerow(
            [
                detect_blank_music(os.path.join(EXAMPLE_DIR, "vocals_full.mp3"), threshold=threshold),
                detect_blank_music(
                    os.path.join(EXAMPLE_DIR, "vocals_blank.mp3"),
                    threshold=threshold,
                ),
            ]
        )
