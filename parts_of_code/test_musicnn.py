# 定義 occur_sum 是邊長為 valid_tags 長度的 0 陣列
# 列數是實際音樂類型在 valid_tags 內的位置，欄數則是預測音樂類型
occur_sum = np.zeros((len(valid_tags), len(valid_tags)))
# occur_len 的大小跟 occur_sum 一樣
occur_len = np.zeros_like(occur_sum)

for i, sample in samples.iterrows():
    # 如果全部音樂類型都已測試了 100 音樂片段
    if occur_len.all() >= 100:
        break  # 停止測試

    sample = sample["music_name"]

    # 得到該音樂片段的所有音樂類型
    genres = generate_prompt(sample, include_tags=False).split()

    # 循環每一個可以被記錄的標註
    for genre_i, genre in enumerate(valid_tags):
        # 如果目前的音樂片段音樂類型是這一個可以被記錄的標註且果這個音樂類型還沒被測試 100 次
        if genre in genres and (occur_len[genre_i] < 100).any()::
            taggram, tags = extractor(
                DATASET_DIR / "split_by_time" / "accompaniment" / f"{sample}.mp3", extract_features=False
            )  # 每一個時間點模型預測出來的標註機率

            tags_likelihood_mean = np.mean(taggram, axis=0)  # 平均所有時間點的機率
            # 將其轉換成標註 -> 機率的字典
            tags_likelihood_mean = dict(zip(tags, tags_likelihood_mean))

            # 循環每個可以被記錄的標註
            for tag_i, tag in enumerate(valid_tags):
                occur_sum[genre_i, tag_i] += tags_likelihood_mean[tag]

            occur_len[genre_i] += 1
