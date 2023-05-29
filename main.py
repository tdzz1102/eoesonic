from concurrent.futures import ThreadPoolExecutor
from app.httpclient import music_search
from app.db import insert_song, get_songs
from app.pull import Pull
from app.config import config


EOE_MEMBERS = ['柚恩', '露早', '米诺', '莞儿', '虞莫']


def sync_db(member):
    pageable, items = music_search(member)
    for song_dict in items:
        insert_song(song_dict)
    
    
def pull_music():
    song_iter = get_songs()
    for song in song_iter:
        # TODO: 异步下载？
        Pull.pull_if_not_exist(song)
    
    
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