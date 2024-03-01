pip install virtualenv

# WebUI

python3.9 -m venv venvs/webui
source venvs/webui/bin/activate
trap 'deactivate; rm -r venvs/webui; exit 0' SIGINT # Do stuff when Ctrl-C

# For Python 3.9.18:

pip install --no-deps -r webui_require.txt

# For people who have python versions not compatible with webui_require.txt:

#pip install gradio
#pip install pydub
#pip install Pillow
#pip install colorama
#pip install transformers
#pip install torch
#pip install torchaudio
#pip install scipy
#pip install spleeter

deactivate

# Dev (WebUI OK, Training REQUIRED, Scraper REQUIRED, Process REQUIRED)
python3.9 -m venv venvs/dev
source venvs/dev/bin/activate
trap 'deactivate; rm -r venvs/dev; exit 0' SIGINT # Do stuff when Ctrl-C

apt-get -y install libc-dev
apt-get -y install build-essential

pip install Cython
pip install --no-deps -r requirements.txt

deactivate

# MusicNN (MusicNN conflicts with every thing, so it is singled out)
#
#
#
#python3.9 -m venv venvs/musicnn
#source venvs/musicnn/bin/activate
#trap 'deactivate; rm -r venvs/musicnn; exit 0' SIGINT # Do stuff when Ctrl-C
#
#python dependencies/musicnn/setup.py install
#
#deactivate