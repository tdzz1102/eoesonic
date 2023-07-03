from app.db import Song, Album, get_song_count
from app.httpclient import get_raw
from app.tools import AtomicInteger
from mutagen.mp4 import MP4, MP4Cover
from loguru import logger
import re
from pathlib import Path
from io import BytesIO
from app.config import Config


class SongPull:
    'pull song in db to local'
    counter = AtomicInteger()
    song_count = get_song_count()
    
    def __init__(self, song: Song, album: Album) -> None:
        self.song = song
        self.album = album
    
    def pull_if_not_exist(self) -> None:
        if not self.get_save_path().is_file(): # if song do not exist
            self.pull()
    
    def get_save_path(self):
        file_path: Path = Path(Config.music_path) / self.album.singer / self.album.live / f"{self.song.downloadFileName}"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        return file_path

    def pull(self) -> None:
        try:
            SongPull.counter.increment()
            logger.info(f'({SongPull.counter.get_value()} / {SongPull.song_count}) pull {self.song.downloadFileName}')
            audio_url = self.song.audioUrl
            if not audio_url.endswith('.m4a'):
                logger.warning('Not a m4a file.')
                return
            audiob = get_raw(self.song.audioUrl)
            audiobio = BytesIO(audiob)
            audiobio_target = BytesIO(audiob)
            m4a = MP4(audiobio)
            
            """set cover"""
            try:
                coverb = get_raw(self.song.coverUrl)
                m4a["covr"] = [MP4Cover(coverb, imageformat=MP4Cover.FORMAT_PNG if self.song.coverUrl.endswith('png') else MP4Cover.FORMAT_JPEG)]
            except Exception as e:
                logger.warning(f'No cover supplyed. The error message is {e}')
            
            """reset album_artist"""
            m4a.tags['aART'] = self.album.singer
                
            """set date"""
            formatted_date = self.song.songDate.strftime("%Y-%m-%d")
            m4a.tags["\xa9day"] = [formatted_date]
            
            """change album title"""
            old_album_tag = m4a.tags["\xa9alb"][0]
            pattern = r"\d{4}年\d{2}月\d{2}日【.+?】(.+)"
            result = re.search(pattern, old_album_tag)
            if result:
                title = result.group(1)
                m4a.tags["\xa9alb"][0] = title
                
            save_path = self.get_save_path()
            m4a.save(audiobio_target)
            with open(str(save_path), 'wb') as f:
                f.write(audiobio_target.getvalue())
        except Exception as e:
            logger.error(e)
        