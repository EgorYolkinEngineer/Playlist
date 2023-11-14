from aiogram.types import (InlineQuery, 
                           InlineQueryResultCachedPhoto)
from aiogram import F, Router

from core.conf.config import bot
from core.conf import config
from core import states
from core.schemas import (UserScheme, 
                          PlaylistScheme, 
                          PlaylistSongScheme)
from core import keyboards
from core.services.playlist_service import playlist_service

inline_router = Router(name="inline")


@inline_router.inline_query()
async def inline_handler(query: InlineQuery):
    playlists = playlist_service.search_playlist(
        query=query.query, 
        user_pk=query.from_user.id
    )

    results = []
    for result_id, playlist in enumerate(playlists):
        playlist_caption = (f"<b>{playlist.name}</b>\n\n" \
                            f"<i>{playlist.description}</i>")
        
        reply_markup = await keyboards.get_listen_playlist_reply_markup(
            playlist_pk=playlist.pk
        )
        results.append(InlineQueryResultCachedPhoto(
            id=str(result_id),
            photo_file_id=playlist.preview_file_id,
            caption=playlist_caption, 
            reply_markup=reply_markup
        ))
        

    await query.answer(results, cache_time=1)