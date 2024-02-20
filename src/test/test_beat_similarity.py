from paths import DATASET_DIR, OUTPUT_DIR, TEST_OUTPUT_DIR, CACHE_DIR, NEXTCLOUD_RIFFUSION_DIR
import os

import librosa
import pandas as pd
from src.test.diff import load_model, run_pipeline
from src.test.aio import aio

model_name = "fp16_lr1e-5_train_base"
checkpoints = OUTPUT_DIR / model_name / "models"

spotify_114k = pd.read_csv(DATASET_DIR / "spotify_114k.csv")
df = pd.DataFrame()


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
    model_path = OUTPUT_DIR / model_name / "models" / checkpoint_name
    pipe = load_model(model_path)

    bpm_similarities = []

    for i, row in pd.read_csv(DATASET_DIR / "validation_sample_1000.csv").iterrows():
        music_name = row["music_name"]
        track_id = music_name.split("_")[0]

        os.makedirs(TEST_OUTPUT_DIR / model_name / checkpoint_name, exist_ok=True)

        ground_truth_path = DATASET_DIR / "split_by_time/accompaniment" / f"{music_name}.mp3"
        input_path = DATASET_DIR / "split_by_time/vocals" / f"{music_name}.mp3"
        output_path = TEST_OUTPUT_DIR / model_name / checkpoint_name / f"{music_name}.mp3"

        ground_truth_bpm = calculate_bpm(ground_truth_path)

        if ground_truth_bpm == 0:
            continue

        genre = spotify_114k.loc[spotify_114k["track_id"] == track_id].iloc[0]["track_genre"]

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

        bpm_similarities.append(bpm_similarity)

        avg_bpm_similarity = sum(bpm_similarities) / len(bpm_similarities)

        with open(TEST_OUTPUT_DIR / "log.txt", "a") as f:
            f.write(
                f"{checkpoint_name} {music_name} {genre} {ground_truth_bpm} {output_bpm} {bpm_similarity} {avg_bpm_similarity}\n"
            )

    return bpm_similarities


single_checkpoint = True

checkpoint_name = "checkpoint-61000"
model_path = OUTPUT_DIR / model_name / checkpoint_name

if single_checkpoint:
    df["hackersong"] = pd.Series(test_beat_similarity("hackersong", "checkpoint-41324", False))


else:
    for checkpoint_name in os.listdir(checkpoints):
        if os.path.isdir(model_path) and checkpoint_name not in ("controlnet", "unet"):
            df[checkpoint_name.split("-")[1]] = test_beat_similarity(checkpoint_name, False)

    df = df.reindex(sorted(df.columns, key=lambda s: int(s)), axis=1)

df.to_csv(TEST_OUTPUT_DIR / "beat_similarity_hackersong.csv")
