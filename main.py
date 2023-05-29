from concurrent.futures import ThreadPoolExecutor
from app.httpclient import music_search
from app.db import insert_song, get_songs_with_album
from app.pull import Pull
from app.config import config
from app.constant import EOE_MEMBERS


def sync_db(member):
    pageable, items = music_search(member)
    for song_dict in items:
        insert_song(song_dict)
    
    
def pull_music():
    song_album_iter = get_songs_with_album()
    for song, album in song_album_iter:
        # TODO: 异步下载？
        Pull.pull_if_not_exist(song, album)
    
    
def main():
    # 进行一次全量拉取
    
    # api -> db
    executor = ThreadPoolExecutor()
    for member in EOE_MEMBERS:
        executor.submit(sync_db, member)
    executor.shutdown()
    
    # db -> local
    pull_music()
    

if __name__ == '__main__':
    main()