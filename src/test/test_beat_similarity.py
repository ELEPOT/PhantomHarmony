from paths import DATASET_DIR, OUTPUT_DIR, TEST_OUTPUT_DIR, CACHE_DIR, NEXTCLOUD_RIFFUSION_DIR
import os

import librosa
import pandas as pd
from src.test.diff import load_model, run_pipeline
from src.test.aio import aio

model_name = "fp16_lr1e-5_train_base"
checkpoints = OUTPUT_DIR / model_name / "models"

spotify_114k = pd.read_csv(DATASET_DIR / "spotify_114k.csv")


def calculate_bpm(path):
    y, sr = librosa.load(path)

    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)

    # beats cannot beat empty because beat[0] will create error
    # beats cannot only have one element because len(beats) - 1 will be 0 and create divide by zero error
    if len(beats) > 1:
        first_beat_time, last_beat_time = librosa.frames_to_time((beats[0], beats[-1]), sr=sr)
        return 60 / ((last_beat_time - first_beat_time) / (len(beats) - 1))

    else:
        return 0


def test_beat_similarity(model_name, checkpoint_name, no_controlnet=False):
    beat_similarities = dict()

    model_path = OUTPUT_DIR / model_name / "models" / checkpoint_name
    pipe = load_model(model_path)

    for i, row in pd.read_csv(DATASET_DIR / "validation_sample_2220.csv").iterrows():
        music_name = row["music_name"]
        genre = row["genre"]

        os.makedirs(TEST_OUTPUT_DIR / model_name / checkpoint_name, exist_ok=True)

        ground_truth_path = DATASET_DIR / "split_by_time/accompaniment" / f"{music_name}.mp3"
        input_path = DATASET_DIR / "split_by_time/vocals" / f"{music_name}.mp3"
        output_path = TEST_OUTPUT_DIR / model_name / checkpoint_name / f"{music_name}.mp3"

        ground_truth_bpm = calculate_bpm(ground_truth_path)

        if ground_truth_bpm == 0:
            continue

        if no_controlnet:
            run_pipeline(pipe, None, TEST_OUTPUT_DIR / "b.png", genre)

        else:
            aio("m2s", input_path, TEST_OUTPUT_DIR / "a.png")
            run_pipeline(pipe, TEST_OUTPUT_DIR / "a.png", TEST_OUTPUT_DIR / "b.png", genre)

        aio("s2m", TEST_OUTPUT_DIR / "b.png", output_path)

        output_bpm = calculate_bpm(output_path)

        if output_bpm == 0:
            continue

        smaller_bpm = min((output_bpm, ground_truth_bpm))
        larger_bpm = max((output_bpm, ground_truth_bpm))

        if abs(smaller_bpm - larger_bpm) > abs(smaller_bpm - larger_bpm / 2):
            larger_bpm /= 2

        bpm_similarity = abs(larger_bpm - smaller_bpm)

        if genre in beat_similarities.keys():
            beat_similarities[genre].append(bpm_similarity)
        else:
            beat_similarities[genre] = [bpm_similarity]

        with open(TEST_OUTPUT_DIR / "log.txt", "a") as f:
            f.write(f"{checkpoint_name} {music_name} {genre} {ground_truth_bpm} {output_bpm} {bpm_similarity}\n")

    # To prevent ValueError: All arrays must be of the same length

    df = pd.DataFrame.from_dict(beat_similarities, orient="index")
    df = df.transpose()

    return df


single_checkpoint = True

checkpoint_name = "checkpoint-61000"
model_path = OUTPUT_DIR / model_name / checkpoint_name

test_beat_similarity("fp16_lr1e-5", checkpoint_name, False).to_csv(TEST_OUTPUT_DIR / "fp16_lr1e-5_bs.csv")
test_beat_similarity("fp16_lr1e-5_train_base", checkpoint_name, False).to_csv(
    TEST_OUTPUT_DIR / "fp16_lr1e-5_train_base_bs.csv"
)
test_beat_similarity("", checkpoint_name, True).to_csv(TEST_OUTPUT_DIR / "no_controlnet_bs.csv")
