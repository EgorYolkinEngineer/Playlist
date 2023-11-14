from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserScheme:
    pk: int | None = None
    telegram_user_id: int | str = None
    nickname: str = None
    
    
@dataclass
class PlaylistScheme:
    pk: int | None = None
    creator_telegram_id: int | str = None
    preview_file_id: str | None = None
    name: str | None = None
    description: str | None = None
    

@dataclass
class PlaylistSongScheme:
    pk: int | None = None
    playlist_pk: int | None = None
    audio_file_id: str | None = None
    is_favorite: bool = False
    created: datetime | None = None
