from app.db import Song, Album
from app.httpclient import get_raw
from mutagen.mp4 import MP4, MP4Cover
from loguru import logger
import re
from pathlib import Path
from io import BytesIO
from app.config import config


class Pull:
    music_path = config.get('navidrome', 'music_path')
    
    @classmethod
    def pull_if_not_exist(cls, song: Song, album: Album) -> None:
        if not cls.check_if_exist(song):
            cls.pull(song, album)
    
    @classmethod
    def get_save_path(cls, song: Song):
        create_month = song.songDate.strftime("%Y-%m")
        file_path: Path = Path(cls.music_path) / create_month / f"{song.downloadFileName}.m4a"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        return file_path
    
    @classmethod
    def check_if_exist(cls, song: Song) -> bool:
        return cls.get_save_path(song).is_file()

    @classmethod
    def pull(cls, song: Song, album: Album) -> None:
        try:
            logger.info(f"Pulling {song.downloadFileName}...")
            audiob = get_raw(song.audioUrl)
            audiobio = BytesIO(audiob)
            audiobio_target = BytesIO(audiob)
            m4a = MP4(audiobio)
            
            """set cover"""
            try:
                coverb = get_raw(song.coverUrl)
                m4a["covr"] = [MP4Cover(coverb, imageformat=MP4Cover.FORMAT_PNG if song.coverUrl.endswith('png') else MP4Cover.FORMAT_JPEG)]
            except Exception as e:
                logger.warning(f'No cover supplyed. The error message is {e}')
            
            """reset album_artist"""
            m4a.tags['aART'] = album.singer
                
            """set date"""
            formatted_date = song.songDate.strftime("%Y-%m-%d")
            m4a.tags["\xa9day"] = [formatted_date]
            
            """change album title"""
            old_album_tag = m4a.tags["\xa9alb"][0]
            pattern = r"\d{4}年\d{2}月\d{2}日【.+?】(.+)"
            result = re.search(pattern, old_album_tag)
            if result:
                title = result.group(1)
                m4a.tags["\xa9alb"][0] = title
                
            save_path = cls.get_save_path(song)
            m4a.save(audiobio_target)
            with open(str(save_path), 'wb') as f:
                f.write(audiobio_target.getvalue())
        except Exception as e:
            logger.error(e)
        