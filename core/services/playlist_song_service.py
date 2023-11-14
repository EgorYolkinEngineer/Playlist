from dataclasses import asdict

from core.gateways.playlist_song_gateway import (PlaylistSongGateway, 
                                                 playlist_song_gateway)

from core.models import PlaylistSong
from core.schemas import PlaylistSongScheme


class PlaylistSongService:
    model: PlaylistSong = PlaylistSong
    
    def __init__(self, 
                 gateway: PlaylistSongGateway
                 ) -> None:
        self.gateway = gateway

    @staticmethod
    def to_scheme(playlist_song: PlaylistSong) -> PlaylistSongScheme:
        scheme = PlaylistSongScheme(
            pk=playlist_song.pk,
            audio_file_id=playlist_song.audio_file_id, 
            is_favorite=playlist_song.is_favorite
        )
        
        return scheme
        
    def create_playlist_song(self, 
                             playlist_song: PlaylistSongScheme
                             ) -> None:
        model = self.model(**asdict(playlist_song))
        self.gateway.create(model)
        
    def get_playlist_songs(self, 
                           playlist_pk: int
                           ) -> list[PlaylistSongScheme]:
        playlist_songs = self.gateway.filter_by(playlist_pk=playlist_pk)
        
        return [self.to_scheme(playlist_song=playlist_song) 
                for playlist_song in playlist_songs]
        

playlist_song_service = PlaylistSongService(gateway=playlist_song_gateway)
