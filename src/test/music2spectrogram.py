import paths
from riffusion.spectrogram_params import SpectrogramParams
from riffusion.spectrogram_image_converter import SpectrogramImageConverter
from pydub import AudioSegment

params = SpectrogramParams()
converter = SpectrogramImageConverter(params)

seg = AudioSegment.from_mp3("/home/leo/v.wav")
converter.spectrogram_image_from_audio(seg).save("/home/leo/v.png")

