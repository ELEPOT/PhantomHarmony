from riffusion.spectrogram_params import SpectrogramParams
from riffusion.spectrogram_image_converter import SpectrogramImageConverter
from PIL import Image

params = SpectrogramParams()
converter = SpectrogramImageConverter(params)

img = Image.open("input path")
converter.audio_from_spectrogram_image(img).export("output path")
