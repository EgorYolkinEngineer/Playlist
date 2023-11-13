from dataclasses import dataclass
from datetime import datetime


@dataclass
class BaseScheme:
    pk: int
    created: datetime


@dataclass
class UserScheme:
    telegram_user_id: int | str
    nickname: str
    
    
@dataclass
class PlaylistScheme:
    preview_file_id: str | None = None
    name: str | None = None
    description: str | None = None
    
    
class PlaylistSongScheme(BaseScheme):
    playlist_pk: int
    audio_file_id: str | None
    is_favorite: bool = False
