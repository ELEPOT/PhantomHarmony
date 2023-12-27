import librosa
import numpy as np
import pydub

filename = "fiction.mp3"

y, sr = librosa.load(filename)

tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

beat_times = librosa.frames_to_time(beat_frames, sr=sr)

for j, sec in enumerate(beat_times):
    if j % 4 == 0:
        print(sec,j)

cropped_y = y[10 * sr:20 * sr]

normalized = True

channels = 2 if (cropped_y.ndim == 2 and cropped_y.shape[1] == 2) else 1
if normalized:  # normalized array - each item should be a float in [-1, 1)
    cropped_y = np.int16(cropped_y * 2 ** 15)
else:
    cropped_y = np.int16(cropped_y)

song = pydub.AudioSegment(cropped_y.tobytes(), frame_rate=sr, sample_width=2, channels=channels)
song.export("bpm_test.mp3", format="mp3", bitrate="320k")
print('ok')
