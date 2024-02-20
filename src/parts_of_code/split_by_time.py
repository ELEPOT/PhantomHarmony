samples_per_section = int(sr * time_per_section)  # 將以時間為單位轉換成以index 為單位


# 開始時間從0秒開始，每次加5.12秒，直到切不出5.12秒為止

for start in range(0, y.size()[0] - samples_per_section, samples_per_section):
    end = start + samples_per_section  # 結束時間 = 開始時間 + 5.12秒

    sep_y = y[start:end]  # 切輸入音檔

    torchaudio.save(os.path.join(out_path, "%s_%05d.mp3" % (track_id, idx)), sep_y, sr)  # 以 “trackid_index”形式作為檔名存檔

    idx += 1
