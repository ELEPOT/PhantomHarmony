# 音樂類型
prompt = spotify_114k.loc[spotify_114k["track_id"] == sample.split("_")[0]].iloc[0]["track_genre"].split(",")

prompt += top_tags(str(DATASET_DIR / "split_by_time" / "accompaniment" / f"{sample}.mp3"), topN=10)  # 音樂標註
prompt = shuffle_slightly(prompt)  # 稍微洗牌順序
prompt = prompt[: randint(1, 11)]  # 隨機擷取前幾個音樂標註

return " ".join(prompt)  # 用空白分隔所有標註
