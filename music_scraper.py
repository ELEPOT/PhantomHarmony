from datasets import load_dataset
import subprocess
import os
import itertools
import shutil


CLIENT_ID = '4dea824b6efe489b9c7c2c0c30822324'
CLIENT_SECRET = 'b22341c0cca242c09e57b1695d512115'

os.environ['SPOTIPY_CLIENT_ID'] = CLIENT_ID
os.environ['SPOTIPY_CLIENT_SECRET'] = CLIENT_SECRET

# modified from https://stackoverflow.com/questions/17547273/flatten-complex-directory-structure-in-python


class Dataset:
    def __init__(self, link_src, uri_column, output_dir=None):
        if output_dir is None:
            self.output_dir = link_src.split('/')[1]
        else:
            self.output_dir = output_dir

        self.dataset = load_dataset(link_src, split='train').shuffle(seed=42)
        self.uri_column = uri_column
        self.index = 0

    def _move(self, destination):
        output_file = ''

        for root, _dirs, files in itertools.islice(os.walk(destination), 1, None):
            for filename in files:
                shutil.move(os.path.join(root, filename), destination)

                output_file = os.path.join(destination, filename)
            os.rmdir(root)

        return output_file

    def pop(self):
        uri = self.dataset[self.uri_column][self.index]
        subprocess.call(['spotify_dl', '-l', f'https://open.spotify.com/track/{uri}', '-o', self.output_dir])
        output_file = self._move(self.output_dir)

        self.index += 1

        return output_file


if __name__ == '__main__':
    dataset = Dataset('maharshipandya/spotify-tracks-dataset', 'track_id')
    print(dataset.pop())
    print(dataset.pop())