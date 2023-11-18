from datasets import load_dataset
import subprocess
import os
import itertools
import shutil
from config import *
import ytmdl

class Dataset:
    def __init__(self, link_src, track_name_col, artists_col, output_dir=None, shuffle=False):
        if output_dir is None:
            self.output_dir = link_src.split('/')[1]
        else:
            self.output_dir = output_dir

        self.dataset = load_dataset(link_src, split='train')

        if shuffle:
            self.dataset = self.dataset.shuffle(seed=4242)

        self.track_name_col = track_name_col
        self.artist_col = artists_col
        self.index = 0
        self.size = self.dataset.num_rows

    def pop(self, log=False):
        track_name = self.dataset[self.track_name_col][self.index]
        artists = self.dataset[self.artist_col][self.index]

        command = [
            'ytmdl',
            track_name,
            '-q',
            '--skip-meta',
            '--ignore-errors',
            '--on-meta-error' ,
            'skip',
            '--artist',
            f'{artists}',
            '-o',
            f'{self.output_dir}',
            '--filename',
            f'{track_name}_{artists}', '--nolocal', '--dont-transcode'
        ]


        if log:
            subprocess.call(command)
        else:
            subprocess.run(command)

        print(command)

        self.index += 1

        return os.path.join(self.output_dir, f'{track_name}_{artists}.mp3')


if __name__ == '__main__':
    dataset = Dataset(
        link_src='maharshipandya/spotify-tracks-dataset',
        track_name_col='track_name',
        artists_col='artists',
        output_dir=f'{DATA_DIR}/dataset/raw_music'
    )

    for i in range(dataset.size):
        dataset.pop(log=True)
