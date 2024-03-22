from paths import VALIDATION_DIR, DATASET_DIR, TEST_OUTPUT_DIR
import librosa
import pandas as pd
import csv
import os


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


def test_beat_similarity(model_name, checkpoint_name="checkpoint-61000"):
    bpm_similarities = []

    for i, row in pd.read_csv(DATASET_DIR / "validation_sample_2220.csv").iterrows():
        music_name = row["music_name"]
        genre = row["genre"]
        tags = row["tags"]

        ground_truth_path = DATASET_DIR / "split_by_time" / "accompaniment" / f"{music_name}.mp3"
        output_path = VALIDATION_DIR / model_name / checkpoint_name / f"{music_name}.mp3"

        ground_truth_bpm = calculate_bpm(ground_truth_path)
        output_bpm = calculate_bpm(output_path)

        if ground_truth_bpm == 0 or output_bpm == 0:
            continue

        bpm_similarity = abs(output_bpm - ground_truth_bpm)
        bpm_similarities.append(bpm_similarity)

        print(sum(bpm_similarities) / len(bpm_similarities), output_bpm / ground_truth_bpm)

        output_csv_path = TEST_OUTPUT_DIR / f"{model_name}_bs.csv"
        file_exists = os.path.isfile(output_csv_path)

        with open(output_csv_path, "a") as f:
            writer = csv.DictWriter(f, fieldnames=["music_name", "genre", "tags", "ground_truth_bpm", "output_bpm"])

            if not file_exists:
                writer.writeheader()

            writer.writerow(
                dict(
                    music_name=music_name,
                    genre=genre,
                    tags=tags,
                    ground_truth_bpm=ground_truth_bpm,
                    output_bpm=output_bpm,
                )
            )


# test_beat_similarity("no_controlnet", "checkpoint-61000")
# test_beat_similarity("0_hackersong", "checkpoint-41324")
# test_beat_similarity("1", "checkpoint-61000")
# test_beat_similarity("2", "checkpoint-61000")
# test_beat_similarity("1_train_base", "checkpoint-61000")
# test_beat_similarity("2_train_base", "checkpoint-61000")
# test_beat_similarity("3_beat_mark", "checkpoint-61000")
# test_beat_similarity("3_beat_mark-[from_accompaniment]", "checkpoint-61000")
# test_beat_similarity("3_beat_mark_train_base-[from_accompaniment]", "checkpoint-61000")
test_beat_similarity("3_beat_mark_train_base", "checkpoint-61000")
