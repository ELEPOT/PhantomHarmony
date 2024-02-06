import paths
from riffusion.spectrogram_params import SpectrogramParams
from riffusion.spectrogram_image_converter import SpectrogramImageConverter
from pydub import AudioSegment
from PIL import Image
import sys
import subprocess
from colorama import *

in_path = str(sys.argv[2])
out_path = str(sys.argv[3])
def run(mode,in_path,out_path):
    if mode == "m2s":
        params = SpectrogramParams()
        converter = SpectrogramImageConverter(params)

        seg = AudioSegment.from_file(in_path)
        seg = seg.set_frame_rate(44100)
        converter.spectrogram_image_from_audio(seg).save(out_path)

    elif mode == "s2m":
        params = SpectrogramParams()
        converter = SpectrogramImageConverter(params)

        img = Image.open(in_path)
        converter.audio_from_spectrogram_image(img).export(out_path)
'''
try:
    if str(sys.argv[1]) == "m2s":
        params = SpectrogramParams()
        converter = SpectrogramImageConverter(params)

        seg = AudioSegment.from_file(in_path)
        seg = seg.set_frame_rate(44100)
        converter.spectrogram_image_from_audio(seg).save(out_path)

    elif str(sys.argv[1]) == "s2m":
        params = SpectrogramParams()
        converter = SpectrogramImageConverter(params)

        img = Image.open(in_path)
        converter.audio_from_spectrogram_image(img).export(out_path)

except:
    help_text = """
    Usage:
        python aio.py (m2s / s2m) (in_path) (out_path)
    
    Commands:
        m2s: 
            Convert music to spectrogram
        s2m: 
            Convert spectrogram to music
    """

    print(Fore.RED + help_text)
'''