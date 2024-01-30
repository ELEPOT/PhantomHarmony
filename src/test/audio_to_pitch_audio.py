import os
import subprocess

import librosa
import numpy as np
import soundfile as sf

from paths import TEST_OUTPUT_DIR, DEPENDENCIES_DIR, VENV_PYTHON_DIR

audio_path = TEST_OUTPUT_DIR / "spleeter" / "fiction" / "vocals.wav"  # Change this to your input audio path

pitch_output_path = TEST_OUTPUT_DIR / "melody"

pitch_audio_output_path = TEST_OUTPUT_DIR / "melody" / "fiction_pitch.wav"  # Change this to desired output path

pitch_file_path = TEST_OUTPUT_DIR / "melody" / f"pitch_{os.path.split(audio_path)[-1]}.txt"

py_file_path = DEPENDENCIES_DIR / "melodyExtraction_JDC/melodyExtraction_JDC.py"

# convert audio to pitch
subprocess.call(
    (
        VENV_PYTHON_DIR,
        py_file_path,
        "-p",
        audio_path,
        "-gpu",
        "0",
        "-o",
        pitch_output_path,
    ),
    cwd=DEPENDENCIES_DIR / "melodyExtraction_JDC",
)

# convert pitch back into audio
y, sr = librosa.load(audio_path, sr=None)

D = librosa.stft(y)
pitch = np.zeros_like(D)

with open(pitch_file_path, "r") as f:
    for row in f:
        t, freq = map(float, row.split())

        frame = np.clip(librosa.time_to_frames(t, sr=sr), 0, pitch.shape[1] - 1)
        diff = np.absolute(librosa.fft_frequencies(sr=sr) - freq)
        freq_bin = diff.argmin()

        pitch[freq_bin, frame] = 1000

sf.write(
    pitch_audio_output_path,
    librosa.griffinlim(pitch),
    samplerate=int(sr),
)
