from datasets import load_dataset
import subprocess
import os
import itertools
import shutil
from config import *
import ytmdl

class Dataset:
    def __init__(self, link_src, track_name_col, artists_col, track_id_col, output_dir=None, shuffle=False, start_index=0, end_index=-1):
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

    def pop(self, log=False):
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


        if log:
            subprocess.call(command)
        else:
            subprocess.run(command)

        print(command)

        return os.path.join(self.output_dir, f'{track_name}_{artists}.mp3')


if __name__ == '__main__':
    dataset = Dataset(
        link_src='maharshipandya/spotify-tracks-dataset',
        track_name_col='track_name',
        artists_col='artists',
        output_dir=f'{DATA_DIR}/dataset/spotify_114k',
        start_index=0,
        end_index=57000
    )

    while True:
        try:
            dataset.pop(log=True)
        except IndexError:
            print('End of dataset!')
            break
