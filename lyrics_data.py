import os
import random
import time


def get_random_song_path() -> dict:
    random.seed(time.time())
    base_dir = os.path.join(os.getcwd(), 'lyrics')
    
    songs_name_dir = []

    for (dirpath, dirnames, filenames) in os.walk(base_dir):
        for item in dirnames:
            songs_name_dir.append(item)
    song_name_dir = random.choice(songs_name_dir)
    return {
        'song_text_path': os.path.join(base_dir, song_name_dir, 'text.txt'),
        'song_name_path': os.path.join(base_dir, song_name_dir, 'name.txt')
    }

def get_song_data(text_path: str, name_path: str) -> dict:
    song_data = {
        'song_text': '',
        'song_name': ''
    }

    with open(text_path, 'r', encoding='UTF-8') as file:
        song_data['song_text'] = file.readlines()

    with open(name_path, 'r', encoding='UTF-8') as file:
        song_data['song_name'] = file.read()

    return song_data

def song() -> dict:
    paths = get_random_song_path()
    data = get_song_data(paths['song_text_path'], paths['song_name_path'])
    return data

if __name__ == '__main__':
    print(song())
