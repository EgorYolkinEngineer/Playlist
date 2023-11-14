from core.gateways.abstract_gateway import AbstractGateway
from core.models import Playlist

from core.conf.database import session, Session


class PlaylistGateway(AbstractGateway):
    def __init__(self, 
                 session: Session):
        self.session = session

    def get(self, pk: int) -> Playlist:
        return self.session.query(Playlist).get(pk)
    
    def get_all(self) -> list[Playlist]:
        return self.session.query(Playlist).all
    
    def filter_by(self, **kwargs) -> list[Playlist]:
        return self.session.query(Playlist).filter_by(**kwargs).all()

    def filter_only(self, filter_expression) -> list[Playlist]:
        return self.session.query(Playlist).filter(filter_expression).all()

    def create(self, playlist: Playlist):
        self.session.add(playlist)
        self.session.commit()

    def update(self, 
               pk: int, 
               playlist: Playlist):
        self.session.query(Playlist).filter(Playlist.pk == pk).update(playlist)
        self.session.commit()

    def delete(self, pk):
        self.session.query(Playlist).filter(Playlist.pk == pk).delete()
        self.session.commit()


playlist_gateway = PlaylistGateway(session=session)