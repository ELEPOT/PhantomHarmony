import paths
from riffusion.spectrogram_params import SpectrogramParams
from riffusion.spectrogram_image_converter import SpectrogramImageConverter
from pydub import AudioSegment
from PIL import Image
import sys

if str(sys.argv[1]) == "m2s":
    params = SpectrogramParams()
    converter = SpectrogramImageConverter(params)

    seg = AudioSegment.from_mp3(str(sys.argv[2]))
    seg = seg.set_frame_rate(44100)
    converter.spectrogram_image_from_audio(seg).save(str(sys.argv[3]))
elif str(sys.argv[1]) == "s2m":
    params = SpectrogramParams()
    converter = SpectrogramImageConverter(params)

    img = Image.open(str(sys.argv[2]))
    converter.audio_from_spectrogram_image(img).export(str(sys.argv[3]))