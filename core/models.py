from sqlalchemy import (Column, Integer, 
                        String, DateTime, 
                        Boolean, ForeignKey)

from datetime import datetime

from core.conf.database import Base, engine


class User(Base):
    __tablename__ = 'users'

    pk = Column(Integer, 
                primary_key=True, 
                autoincrement=True)
    telegram_user_id = Column(Integer, 
                              unique=True)
    nickname = Column(String)
    created = Column(DateTime)


class Playlist(Base):
    __tablename__ = 'playlists'

    pk = Column(Integer, primary_key=True, autoincrement=True)
    creator_telegram_id = Column(Integer)
    
    preview_file_id = Column(String)
    name = Column(String)
    description = Column(String)
    created = Column(DateTime)


class PlaylistSong(Base):
    __tablename__ = 'playlist_songs'

    pk = Column(Integer, 
                primary_key=True, 
                autoincrement=True)
    playlist_pk = Column(Integer, 
                         ForeignKey('playlists.pk'))
    audio_file_id = Column(String)
    is_favorite = Column(Boolean, default=False)
    created = Column(DateTime, 
                     default=datetime.now())


Base.metadata.create_all(engine)