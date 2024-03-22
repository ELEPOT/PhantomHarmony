from paths import DATASET_DIR, OUTPUT_DIR, VALIDATION_DIR
import os

import pandas as pd
from src.test.diff import load_model, run_pipeline
from src.test.aio import aio
from src.process.mark_beat import mark_beat

model_name = "fp16_lr1e-5_train_base"
checkpoints = OUTPUT_DIR / model_name / "models"


def run_validation(
    model_name=None,
    checkpoint_name=None,
    include_tags=False,
    include_beat_mark=False,
    beat_from_vocals=True,
    output_name=model_name,
):
    no_controlnet = not model_name or not checkpoint_name

    model_path = OUTPUT_DIR / model_name / "models" / checkpoint_name
    pipe = load_model(model_path)

    os.makedirs(VALIDATION_DIR / output_name / checkpoint_name, exist_ok=True)

    for i, row in pd.read_csv(DATASET_DIR / "validation_sample_2220.csv").iterrows():
        music_name = row["music_name"]

        if include_tags:
            prompt = row["tags"]
        else:
            prompt = row["genre"]

        input_path = DATASET_DIR / "split_by_time/vocals" / f"{music_name}.mp3"
        ground_truth_path = DATASET_DIR / "split_by_time" / "accompaniment" / f"{music_name}.mp3"
        output_path = VALIDATION_DIR / output_name / checkpoint_name / f"{music_name}.mp3"

        if os.path.isfile(output_path):
            continue

        if no_controlnet:
            run_pipeline(pipe, None, VALIDATION_DIR / "b.png", prompt)

        else:
            aio("m2s", input_path, VALIDATION_DIR / "a.png")

            if include_beat_mark:
                if beat_from_vocals:
                    mark_beat(VALIDATION_DIR / "a.png", input_path, VALIDATION_DIR / "a.png")
                else:
                    mark_beat(VALIDATION_DIR / "a.png", ground_truth_path, VALIDATION_DIR / "a.png")

            run_pipeline(pipe, VALIDATION_DIR / "a.png", VALIDATION_DIR / "b.png", prompt)

        aio("s2m", VALIDATION_DIR / "b.png", output_path)


checkpoint_name = "checkpoint-61000"

# run_validation("1", checkpoint_name)
# run_validation("1_train_base", checkpoint_name)
# run_validation("2", checkpoint_name, include_tags=True)
# run_validation("2_train_base", checkpoint_name, include_tags=True)
# run_validation("1_pep=0.1", checkpoint_name)
# run_validation("0_hackersong", "checkpoint-41324")
# run_validation("1_lr2.56e-3_gas256", checkpoint_name)
# run_validation("no_controlnet")
# run_validation("3_beat_mark", checkpoint_name, include_tags=True, include_beat_mark=True, beat_from_vocals=True)
# run_validation(
#     "3_beat_mark",
#     checkpoint_name,
#     include_tags=True,
#     include_beat_mark=True,
#     beat_from_vocals=False,
#     output_name="3_beat_mark-[from_accompaniment]",
# )
run_validation(
    "3_beat_mark_train_base",
    checkpoint_name,
    include_tags=True,
    include_beat_mark=True,
    beat_from_vocals=True,
    output_name="3_beat_mark_train_base",
)
# run_validation(
#     "3_beat_mark_train_base",
#     checkpoint_name,
#     include_tags=True,
#     include_beat_mark=True,
#     beat_from_vocals=False,
#     output_name="3_beat_mark_train_base-[from_accompaniment]",
# )
