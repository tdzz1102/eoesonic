from app.db import Song
from app.httpclient import get_raw
from mutagen.mp4 import MP4, MP4Cover
from loguru import logger
import re
from pathlib import Path
from io import BytesIO


class Pull:

    # 依赖注入
    music_path = None
    
    @classmethod
    def pull(cls, song: Song) -> None:
        if not cls._check_if_exist(song):
            cls._pull(song)
            
            
    @classmethod
    def _get_save_path(cls, song: Song):
        create_month = song.songDate.strftime("%Y-%m")
        file_path: Path = Path(cls.music_path) / create_month / f"{song.id}.m4a"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        return file_path
    
    @classmethod
    def _check_if_exist(cls, song: Song) -> bool:
        return cls._get_save_path(song).is_file()

    @classmethod
    def _pull(cls, song: Song) -> None:
        try:
            # TODO: 其他其实不重要，希望保证只要歌曲能下载就能导入，其他处理如果失败就变成default就好
            logger.info(f"Pulling {song.downloadFileName}...")
            audiob = get_raw(song.audioUrl)
            audiobio = BytesIO(audiob)
            audiobio_target = BytesIO(audiob)
            m4a = MP4(audiobio)
            
            """set cover"""
            coverb = get_raw(song.coverUrl)
            m4a["covr"] = [MP4Cover(coverb, imageformat=MP4Cover.FORMAT_PNG if song.coverUrl.endswith('png') else MP4Cover.FORMAT_JPEG)]
            
            """unset album_artist"""
            if 'aART' in m4a.tags:
                del m4a.tags['aART']
                
            """set date"""
            formatted_date = song.songDate.strftime("%Y-%m-%d")
            m4a.tags["\xa9day"][0] = formatted_date
            
            """change album name"""
            old_album_tag = m4a.tags["\xa9alb"][0]
            pattern = r"\d{4}年\d{2}月\d{2}日【.+?】(.+)"
            result = re.search(pattern, old_album_tag)
            if result:
                title = result.group(1)
                m4a.tags["\xa9alb"][0] = title
                
            save_path = cls._get_save_path(song)
            m4a.save(audiobio_target)
            with open(str(save_path), 'wb') as f:
                f.write(audiobio_target.getvalue())
        except Exception as e:
            logger.error(e)
            # raise e
        