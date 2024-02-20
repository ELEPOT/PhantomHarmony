if genre in genre_count.keys():  # 如果此音樂類型的數量已被紀錄 (為了避免字典鍵不存在錯誤)
    genre_count[genre] += 1
else:
    genre_count[genre] = 1
