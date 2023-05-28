from app.db import Song
import requests
from mutagen.mp4 import MP4, MP4Cover
from loguru import logger
import re
from pathlib import Path


class Pull:

    # 依赖注入
    music_path = None
    
    @classmethod
    def pull_if_not_exist(cls, song: Song) -> None:
        # check if exist
        pass

    @classmethod
    def pull(cls, song: Song) -> None:
        try:
            # TODO: 其他其实不重要，希望保证只要歌曲能下载就能导入，其他处理如果失败就变成default就好
            audiob = requests.get(song.audioUrl).content
            m4a = MP4(audiob)
            
            """set cover"""
            coverb = requests.get(song.coverUrl).content
            m4a["covr"] = [MP4Cover(coverb, imageformat=MP4Cover.FORMAT_PNG if song.coverUrl.endswith('png') else MP4Cover.FORMAT_JPEG)]
            
            """unset album_artist"""
            if 'aART' in m4a.tags:
                del m4a.tags['aART']
                
            """set date"""
            formatted_date = song.songDate.strftime("%Y-%m-%d")
            m4a.tags["\xa9day"][0] = formatted_date
            
            """change album name"""
            old_album_tag = m4a.tags["\xa9alb"][0]
            # print(old_album_tag)
            pattern = r"\d{4}年\d{2}月\d{2}日【.+?】(.+)"
            result = re.search(pattern, old_album_tag)
            if result:
                title = result.group(1)
                m4a.tags["\xa9alb"][0] = title
                
            save_path = Path(cls.music_path) / f'{song.id}.m4a'
            m4a.save(str(save_path))
            
        except Exception as e:
            logger.error(e)
        