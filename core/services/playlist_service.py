from dataclasses import asdict

from core.gateways.playlist_gateway import (PlaylistGateway, 
                                            playlist_gateway)

from core.models import Playlist
from core.schemas import PlaylistScheme


class UserService:
    model: User = User
    
    def __init__(self, 
                 gateway: PlaylistGateway
                 ) -> None:
        self.gateway = gateway
        
    def create_playlist(self, 
                        playlist: PlaylistScheme
                        ) -> None:
        model = self.model(**asdict(playlist))
        self.gateway.create(model)
        

playlist_service = PlaylistService(gateway=playlist_gateway)