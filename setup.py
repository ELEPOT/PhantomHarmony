import subprocess

subprocess.call(['pip', 'install', '-r', 'requirements.txt'])
subprocess.call(['pip', 'install', '-e', 'diffusers/'])
