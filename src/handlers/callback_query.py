from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F, Router

from core.conf.config import bot
from core.conf import config
from core import states
from core import keyboards

from core.schemas import (UserScheme, 
                          PlaylistScheme, 
                          PlaylistSongScheme)

from core.services.user_service import user_service
from core.services.playlist_service import playlist_service
from core.services.playlist_song_service import playlist_song_service


callback_query_router = Router(name="inline_query")


@callback_query_router.callback_query(
    states.PlaylistSongStatesGroup.select_save_playlist
)
async def select_song_playlist(msg: CallbackQuery, 
                               state: FSMContext):
    state_data = await state.get_data()
    audio_file_id = state_data["audio_file_id"]
    playlist_pk = int(msg.data)
    
    playlist_song = PlaylistSongScheme(
        playlist_pk=playlist_pk, 
        audio_file_id=audio_file_id
    )
    
    playlist_song_service.create_playlist_song(
        playlist_song=playlist_song
    )
    
    playlist = playlist_service.get_playlist(
        playlist_pk=playlist_pk
    )
    
    answer = f"🎧 Трек добавлен в плейлист «{playlist.name}»"
    await msg.message.edit_text(text=answer)
    
    await state.clear()


@callback_query_router.callback_query(
    F.data.startswith("delete_playlist_")
)
async def delete_playlist(msg: CallbackQuery):
    playlist_pk = int(
        msg.data.split("delete_playlist_")[1]
    )
    
    playlist = playlist_service.get_playlist(
        playlist_pk=playlist_pk
    )
    
    playlist_service.delete_playlist(
        playlist_pk=playlist_pk
    )
    
    answer = (f"🗑️ Плейлист «{playlist.name}» " \
              f"({playlist.description}) удалён")
    
    await msg.message.delete()
    await msg.message.answer(text=answer)
