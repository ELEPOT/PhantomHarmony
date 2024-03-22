import pandas as pd
import os
from paths import DATASET_DIR
from musicnn.tagger import top_tags
from random import gauss, randint


spotify_114k = pd.read_csv(DATASET_DIR / "spotify_114k.csv")


def shuffle_slightly(x, orderliness=0.5):
    # 以每一項的項目數為平均數生成常態分佈的隨機值，然後依照這個隨機值為為順序進行重新排列
    x = sorted(enumerate(x), key=lambda i: gauss(i[0] * orderliness, 1))
    return list(dict(x).values())


def generate_prompt(sample, include_tags=True):
    prompt = spotify_114k.loc[spotify_114k["track_id"] == sample.split("_")[0]].iloc[0]["track_genre"].split(",")

    if include_tags:
        prompt += top_tags(str(DATASET_DIR / "split_by_time" / "accompaniment" / f"{sample}.mp3"), topN=10)
        prompt = shuffle_slightly(prompt)
        prompt = prompt[: randint(1, 11)]

    return " ".join(prompt)


if __name__ == "__main__":
    samples = pd.read_csv(DATASET_DIR / "split_by_time_sample.csv")
    df = pd.read_json(DATASET_DIR / "spectrogram" / "train.jsonl", orient="records", lines=True)

    vocals_paths = []
    vocals_beat_mark_paths = []
    accompaniment_paths = []
    prompts_with_tags = []
    prompts_with_genre = []

    for i, sample in samples.iterrows():
        sample = sample["music_name"]

        vocals_paths.append(os.path.join("vocals", sample + ".png"))
        accompaniment_paths.append(os.path.join("accompaniment", sample + ".png"))
        vocals_beat_mark_paths.append(os.path.join("vocals_beat_mark", sample + ".png"))

        tags = generate_prompt(sample)
        genre = generate_prompt(sample, include_tags=False)
        prompts_with_tags.append(tags)
        prompts_with_genre.append(genre)

    df = pd.DataFrame()

    df["prompt_with_tags"] = prompts_with_tags
    df["prompt_with_genre"] = prompts_with_genre
    df["image"] = accompaniment_paths
    df["conditioning_image"] = vocals_paths
    df["conditioning_image_with_beat_mark"] = vocals_beat_mark_paths

    df.to_json(DATASET_DIR / "spectrogram" / "_train.jsonl", orient="records", lines=True)
