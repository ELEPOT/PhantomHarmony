from paths import DATASET_DIR, VALIDATION_DIR, TEST_OUTPUT_DIR

import pandas as pd
from musicnn.tagger import top_tags
import csv
import os


def test_genre_similarity(model_name, checkpoint_name="checkpoint-61000"):
    for i, row in pd.read_csv(DATASET_DIR / "validation_sample_2220.csv").iterrows():
        music_name = row["music_name"]
        ground_truth_genre = row["genre"]
        ground_truth_tags = row["tags"]

        if ground_truth_tags == "new-age":
            ground_truth_genre = "new age"

        output_path = VALIDATION_DIR / model_name / checkpoint_name / f"{music_name}.mp3"

        output_tags = top_tags(str(output_path), topN=10)

        output_csv_path = TEST_OUTPUT_DIR / f"{model_name}_gs.csv"
        file_exists = os.path.isfile(output_csv_path)

        with open(output_csv_path, "a") as f:
            writer = csv.DictWriter(
                f, fieldnames=["music_name", "ground_truth_genre", "ground_truth_tags", "output_tags"]
            )

            if not file_exists:
                writer.writeheader()

            writer.writerow(
                dict(
                    music_name=music_name,
                    ground_truth_genre=ground_truth_genre,
                    ground_truth_tags=ground_truth_tags,
                    output_tags=output_tags,
                )
            )


# test_genre_similarity("1")
# test_genre_similarity("1_train_base")
# test_genre_similarity("2")
# test_genre_similarity("2_train_base")
# test_genre_similarity("0_hackersong", checkpoint_name="checkpoint-41324")
# test_genre_similarity("3_beat_mark")
# test_genre_similarity("3_beat_mark_train_base-[from_accompaniment]")
# test_genre_similarity("3_beat_mark-[from_accompaniment]")
# test_genre_similarity("3_beat_mark_train_base-[from_accompaniment]")
# test_genre_similarity("3_beat_mark_train_base", "checkpoint-61000")
test_genre_similarity("no_controlnet")
