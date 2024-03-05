blank_detect = shuffle(blank_detect)  # 打亂所有音樂片段

name = row["music_name"].split("_")[0]  # 從音樂片段名得到此音樂的track_id
if name in n_of_segments_sampled_for_each_song.keys():  # 如果已有紀錄此音樂片段track_id的取樣次數 (為了避免字典鍵不存在錯誤)
    if n_of_segments_sampled_for_each_song[name] >= N:  # 如果同track_id的音樂片段已被取樣過N次 (N = 4)
        continue  # 跳過

if row["vocals_blank"] < 0.3 and row["accompaniment_blank"] < 0.7:  # 如果符合取樣條件
    if name in n_of_segments_sampled_for_each_song.keys():  # 如果已有紀錄此音樂片段track_id的取樣次數 (為了避免字典鍵不存在錯誤)
        n_of_segments_sampled_for_each_song[name] += 1
    else:
        n_of_segments_sampled_for_each_song[name] = 1

    sampled_music.append(row["music_name"])  # 把此音樂片段加入採樣集內
