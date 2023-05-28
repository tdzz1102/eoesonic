# defination of Song table

from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError
from contextlib import contextmanager
from datetime import datetime

# データベースへの接続エンジンを作成
# TODO: db也加入到配置项中
engine = create_engine('postgresql://luzao:1018@127.0.0.1:5432/luzao')

# Baseオブジェクトを作成
Base = declarative_base()

# テーブルの定義
class Song(Base):
    __tablename__ = 'songs'
    
    id = Column(String, primary_key=True)
    songDate = Column(Date)
    singer = Column(String)
    songName = Column(String)
    songNameAlias = Column(String)
    versionRemark = Column(String)
    audioUrl = Column(String)
    coverUrl = Column(String)
    duration = Column(Integer)
    songLanguage = Column(String)
    songStatus = Column(String)
    hitCount = Column(Integer)
    hasCover = Column(Boolean)
    insertTime = Column(DateTime)
    live = Column(String)
    bv = Column(String)
    hasLyric = Column(Boolean)
    thumbnailUrl = Column(String)
    lyricUrl = Column(String)
    downloadFileName = Column(String)

# テーブルを作成
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """セッションスコープのコンテキストマネージャ"""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()


def insert_song(song_dict: dict):
    with session_scope() as session:
        existing_song = session.query(Song).filter_by(id=song_dict["id"]).first()
        if existing_song: return
        
        song_dict["songDate"] = song_date = datetime.strptime(song_dict["songDate"], "%Y.%m.%d").date()
        song_dict["insertTime"] = song_date = datetime.strptime(song_dict["insertTime"], "%Y-%m-%d %H:%M:%S.%f")
        try:
            song = Song(**song_dict)
            session.add(song)
            session.commit()
        except IntegrityError as e:
            session.rollback()
        
        
def get_songs():
    with session_scope() as session:
        return session.query(Song)