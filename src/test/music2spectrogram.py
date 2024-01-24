from riffusion.spectrogram_params import SpectrogramParams
from riffusion.spectrogram_image_converter import SpectrogramImageConverter
from pydub import AudioSegment

params = SpectrogramParams()
converter = SpectrogramImageConverter(params)

seg = AudioSegment.from_mp3("/mnt/c/Users/elepo/Downloads/shape_of_you.mp3")
converter.spectrogram_image_from_audio(seg).save("/mnt/c/Users/elepo/Downloads/shape_of_you.png")
