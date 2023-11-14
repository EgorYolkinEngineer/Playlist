from sqlalchemy import or_
from dataclasses import asdict

from core.gateways.playlist_gateway import (PlaylistGateway, 
                                            playlist_gateway)

from core.models import Playlist
from core.schemas import PlaylistScheme


class PlaylistService:
    model: Playlist = Playlist
    
    def __init__(self, 
                 gateway: PlaylistGateway
                 ) -> None:
        self.gateway = gateway

    @staticmethod
    def to_scheme(playlist: Playlist) -> PlaylistScheme:
        scheme = PlaylistScheme(
            pk=playlist.pk,
            creator_telegram_id=playlist.creator_telegram_id,
            preview_file_id=playlist.preview_file_id, 
            name=playlist.name, 
            description=playlist.description
        )
        
        return scheme
        
    def get_playlist(self, 
                     playlist_pk: int
                     ) -> PlaylistScheme:
        playlist = self.gateway.get(pk=playlist_pk)
        return self.to_scheme(playlist) if playlist else None
        
    def create_playlist(self, 
                        playlist: PlaylistScheme
                        ) -> None:
        model = self.model(**asdict(playlist))
        self.gateway.create(model)
        
    def delete_playlist(self, 
                        playlist_pk: int
                        ) -> None:
        self.gateway.delete(pk=playlist_pk)
        
    def get_user_playlists(self, 
                           user_pk: int
                           ) -> list[PlaylistScheme]:
        playlists = self.gateway.filter_by(creator_telegram_id=user_pk)
        
        return [self.to_scheme(playlist=playlist) 
                for playlist in playlists]
        
    def search_playlist(self, 
                        query: str, 
                        user_pk: int
                        ) -> PlaylistScheme | None:
        playlists = self.gateway.filter_only(
            or_(
                Playlist.name.ilike(f'%{query}%'),
                Playlist.description.ilike(f'%{query}%')
            )
        )
        
        return [self.to_scheme(playlist=playlist) 
                for playlist in playlists]
        

playlist_service = PlaylistService(gateway=playlist_gateway)