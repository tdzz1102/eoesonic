from app.httpclient import music_search
from app.db import insert_song, get_songs_with_album
from app.pull import SongPull
from app.constant import EOE_MEMBERS
from loguru import logger
from concurrent.futures import ThreadPoolExecutor
import argparse


def sync_db(member):
    pageable, items = music_search(member)
    for song_dict in items:
        insert_song(song_dict)
    
    
def pull_music():
    song_album_iter = get_songs_with_album()
    with ThreadPoolExecutor(max_workers=5) as executor:
        for song, album in song_album_iter:
            sp = SongPull(song, album)
            executor.submit(sp.pull_if_not_exist)
    

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["sync", "pull"], help="Specify the command to execute: sync or pull")
    return parser.parse_args()
    
    
def main():
    args = parse_arguments()
    
    if args.command == "sync":
        for member in EOE_MEMBERS:
            logger.debug(member)
            sync_db(member)
        
    elif args.command == "pull":
        pull_music()
        
    else:
        logger.error("Invalid command specified.")


if __name__ == '__main__':
    main()