from datasets import load_dataset
import subprocess
import os
import itertools
import shutil
from config import *
import ytmdl
import yaml

class Dataset:
    def __init__(self, link_src, track_name_col, artists_col, track_id_col, output_dir=None, shuffle=True, start_index=0, end_index=-1):
        if output_dir is None:
            self.output_dir = link_src.split('/')[1]
        else:
            self.output_dir = output_dir

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        self.dataset = load_dataset(link_src, split='train')

        if shuffle:
            self.dataset = self.dataset.shuffle(seed=4242)

        self.dataset = self.dataset.to_list()

        if end_index == -1:
            self.dataset = self.dataset[start_index:]
        else:
            self.dataset = self.dataset[start_index:end_index]

        self.track_name_col = track_name_col
        self.artist_col = artists_col
        self.track_id_col = track_id_col
    
    def _track_already_downloaded(self, track_id):
        return os.path.exists(os.path.join(self.output_dir, track_id + '.mp3'))
        
    def _run_command_with_timeout(self, command, timeout):
        print(command)
        
        try:
            subprocess.run(command, timeout=timeout)
        except subprocess.TimeoutExpired:
            print("Command took too long. Probably false files that are too big")
    
    def pop(self):
        row = self.dataset.pop(0)

        track_name = row[self.track_name_col]
        artists = row[self.artist_col]
        track_id = row[self.track_id_col]

        command = [
            'ytmdl',
            track_name,
            '-q',
            '--skip-meta',
            '--ignore-errors',
            '--on-meta-error' ,
            'skip',
            '--artist',
            artists,
            '-o',
            f'{self.output_dir}',
            '--filename',
            track_id, '--nolocal', '--dont-transcode'
        ]
        
        artist_not_found_command = [
            'ytmdl',
            track_name,
            '-q',
            '--skip-meta',
            '--ignore-errors',
            '--on-meta-error' ,
            'skip',
            '-o',
            f'{self.output_dir}',
            '--filename',
            track_id, '--nolocal', '--dont-transcode'
        ]
        
        if self._track_already_downloaded(track_id):
            print(f'Skipping {track_id}')
            return

        if os.path.isfile('bad_files.txt'):
            with open('bad_files.txt', 'r') as f:
                if track_id in [s.rstrip('\n') for s in f.readlines()]:
                    print(f'Skipping {track_id} because it is known to be large or not findable')
                    return

        if artists is None or track_name is None:
            print('Skipping files with no track_name or artist info')
            return

        self._run_command_with_timeout(command, timeout=15)
        
        if self._track_already_downloaded(track_id):
            return os.path.join(self.output_dir, f'{track_name}_{artists}.mp3')

        print("Failed. Trying not use artist info...")
        
        self._run_command_with_timeout(artist_not_found_command, timeout=15)
         
        if self._track_already_downloaded(track_id):
            return os.path.join(self.output_dir, f'{track_name}_{artists}.mp3')
        
        print('Cannot find song or both tries take too long')

        with open('bad_files.txt', 'a') as f:
            f.write(track_id + '\n')
        
        return 404
    

if __name__ == '__main__':
    dataset = Dataset(
        link_src='maharshipandya/spotify-tracks-dataset',
        track_name_col='track_name',
        artists_col='artists',
        track_id_col='track_id',
        output_dir=f'{DATA_DIR}/dataset/spotify_114k',
        start_index=95000,
    )

    while True:
        try:
            dataset.pop()
        except IndexError:
            print('End of dataset!')
            break
