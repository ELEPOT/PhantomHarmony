from paths import DATASET_DIR, OUTPUT_DIR, TEST_OUTPUT_DIR, CACHE_DIR
import os

import librosa
import pandas as pd
from src.test.diff import load_model, run_pipeline
from src.test.aio import aio

checkpoints = OUTPUT_DIR / "fp16_lr1e-5_train_base/models"
spotify_114k = pd.read_csv(DATASET_DIR / "spotify_114k.csv")
df = pd.DataFrame()

for checkpoint_name in os.listdir(checkpoints):
    model_path = checkpoints / checkpoint_name

    if os.path.isdir(model_path) and checkpoint_name not in ("controlnet", "unet"):
        pipe = load_model(model_path)
        bpm_similarities = []

        for i, row in pd.read_csv(DATASET_DIR / "validation_sample.csv").iterrows():
            music_name = row["music_name"]
            track_id = music_name.split("_")[0]

            os.makedirs(TEST_OUTPUT_DIR / "fp16_lr1e-5_train_base" / checkpoint_name, exist_ok=True)

            input_path = DATASET_DIR / "split_by_time/accompaniment" / f"{music_name}.mp3"
            output_path = TEST_OUTPUT_DIR / "fp16_lr1e-5_train_base" / checkpoint_name / f"{music_name}.mp3"

            y, sr = librosa.load(input_path)
            original_bpm = librosa.beat.tempo(y=y, sr=sr)[0]

            genre = spotify_114k.loc[spotify_114k["track_id"] == track_id].iloc[0]["track_genre"]

            aio("m2s", input_path, TEST_OUTPUT_DIR / "a.png")
            run_pipeline(pipe, TEST_OUTPUT_DIR / "a.png", TEST_OUTPUT_DIR / "b.png", genre)
            aio("s2m", TEST_OUTPUT_DIR / "b.png", output_path)

            y, sr = librosa.load(output_path)
            output_bpm = librosa.beat.tempo(y=y, sr=sr)[0]

            bpm_similarity = abs(output_bpm - original_bpm)

            bpm_similarities.append(bpm_similarity)

            avg_bpm_similarity = sum(bpm_similarities) / len(bpm_similarities)

            with open(TEST_OUTPUT_DIR / "log.txt", "a") as f:
                f.write(
                    f"{checkpoint_name} {music_name} {genre} {original_bpm} {output_bpm} {bpm_similarity} {avg_bpm_similarity}\n"
                )

        df[checkpoint_name.split("-")[1]] = bpm_similarities

df = df.reindex(sorted(df.columns, key=lambda s: int(s)), axis=1)
df.to_csv(TEST_OUTPUT_DIR / "fp16_lr1e-5_train_base_beat_similarity.csv")
