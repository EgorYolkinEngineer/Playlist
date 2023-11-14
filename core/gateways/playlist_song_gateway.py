from core.gateways.abstract_gateway import AbstractGateway
from core.models import PlaylistSong

from core.conf.database import session, Session


class PlaylistSongGateway(AbstractGateway):
    def __init__(self, 
                 session: Session):
        self.session = session

    def get(self, pk: int) -> PlaylistSong:
        return self.session.query(PlaylistSong).get(pk)
    
    def get_all(self) -> list[PlaylistSong]:
        return self.session.query(PlaylistSong).all
    
    def filter_by(self, **kwargs) -> list[PlaylistSong]:
        return self.session.query(PlaylistSong).filter_by(**kwargs).all()

    def create(self, playlist_song: PlaylistSong):
        self.session.add(playlist_song)
        self.session.commit()
        
    def delete(self, pk):
        self.session.query(PlaylistSong).filter(PlaylistSong.pk == pk).delete()
        self.session.commit()


playlist_song_gateway = PlaylistSongGateway(session=session)