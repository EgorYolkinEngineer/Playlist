from core.gateways.abstract_gateway import AbstractGateway
from core.models import Playlist

from core.conf.database import session, Session


class PlaylistGateway(AbstractGateway):
    def __init__(self, 
                 session: Session):
        self.session = session

    def get(self, id: int) -> Playlist:
        return self.session.query(Playlist).get(id)

    def create(self, playlist: Playlist):
        self.session.add(playlist)
        self.session.commit()

    def update(self, 
               pk: int, 
               user: Playlist):
        self.session.query(Playlist).filter(Playlist.pk == pk).update(user)
        self.session.commit()

    def delete(self, pk):
        self.session.query(Playlist).filter(Playlist.pk == pk).delete()
        self.session.commit()


playlist_gateway = PlaylistGateway(session=session)