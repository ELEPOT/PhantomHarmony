from src.process.batch_blank_detect import detect_blank_music
import numpy as np
from paths import EXAMPLE_DIR, TEST_OUTPUT_DIR
import os
import pandas as pd

pd.DataFrame(
    [
        [
            threshold,
            "有聲",
            detect_blank_music(os.path.join(EXAMPLE_DIR, "vocals_full.mp3"), threshold=threshold),
        ]
        for threshold in np.arange(0, 0.05, 0.0005)
    ]
    + [
        [
            threshold,
            "無聲",
            detect_blank_music(
                os.path.join(EXAMPLE_DIR, "vocals_blank.mp3"),
                threshold=threshold,
            ),
        ]
        for threshold in np.arange(0, 0.05, 0.0005)
    ],
    columns=["臨界值 (librosa.load)", "段落類別", "音檔數值低於臨界值的相對次數 (%)"],
).to_csv(TEST_OUTPUT_DIR / "blank_threshold.csv")
