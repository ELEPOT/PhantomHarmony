_, beats = librosa.beat.beat_track(y=y, sr=sr)  # 計算拍點位置

# beats 不能是空的因為 beat[0] 會有項目不存在錯誤
# beats 不能只有一項因為 len(beats) - 1 會是 0 然後造成不能除以零的錯誤
if len(beats) > 1:
    # 得到第一個跟最後一個拍點，並將其單位從index轉成時間
    first_beat_time, last_beat_time = librosa.frames_to_time((beats[0], beats[-1]), sr=sr)
    # 回傳 BPM
    return 60 / ((last_beat_time - first_beat_time) / (len(beats) - 1))

else:
    # 無法由資料得知BPM，回傳 0
    return 0


smaller_bpm = min((output_bpm, ground_truth_bpm))
larger_bpm = max((output_bpm, ground_truth_bpm))

# abs 是絕對值的意思
if abs(smaller_bpm - larger_bpm) > abs(smaller_bpm - larger_bpm / 2):
    larger_bpm /= 2

bpm_similarity = abs(larger_bpm - smaller_bpm)
