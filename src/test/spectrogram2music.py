import paths
from riffusion.spectrogram_params import SpectrogramParams
from riffusion.spectrogram_image_converter import SpectrogramImageConverter
from PIL import Image

params = SpectrogramParams()
converter = SpectrogramImageConverter(params)

img = Image.open("/home/leo/stable-diffusion-webui/outputs/txt2img-images/2024-01-30/00002-1692901518.png")
converter.audio_from_spectrogram_image(img).export("/home/leo/test.mp3")
