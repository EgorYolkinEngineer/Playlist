from aiogram.types import Message
from aiogram.types import FSInputFile
from aiogram.filters import (Command, 
                             CommandStart)
from aiogram.fsm.context import FSMContext
from aiogram import F, Router

import asyncio, os

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


messages_router = Router(name="messages")


def get_msg_arg(msg_text: str) -> str | None:
    arg = msg_text.split(" ", maxsplit=1)[1]
    if arg:
        return arg

   
async def send_playlist_songs_to_user(msg: Message, 
                                      playlist_pk: PlaylistScheme):
    playlist_songs = playlist_song_service.get_playlist_songs(
        playlist_pk=playlist_pk
    )
    
    for playlist_song in playlist_songs:
        await msg.answer_audio(
            audio=playlist_song.audio_file_id
        )

    
async def send_playlist_to_user(msg: Message, 
                                playlist: PlaylistScheme):
    if playlist:
        playlist_caption = (f"<b>{playlist.name}</b>\n\n" \
                            f"<i>{playlist.description}</i>\n\n")
        
        playlist_songs = playlist_song_service.get_playlist_songs(
            playlist_pk=playlist.pk
        )
        
        reply_markup = keyboards.get_share_playlist_reply_markup(
            playlist=playlist, 
            delete_button=msg.from_user.id == playlist.creator_telegram_id
        )
            
        await msg.answer_photo(photo=playlist.preview_file_id, 
                            caption=playlist_caption, 
                            reply_markup=reply_markup)
        
        await send_playlist_songs_to_user(
            msg=msg, 
            playlist_pk=playlist.pk
        )
    else:
        answer = "🗑️ Плейлиста не существует"
        await msg.answer(text=answer)


@messages_router.message(CommandStart(), 
                         get_msg_arg(msg_text=F.text))
async def start_arg_message(msg: Message):
    playlist_pk: str = int(
        get_msg_arg(msg.text).split("playlist_")[1]
    )
    playlist = playlist_service.get_playlist(
        playlist_pk=playlist_pk
    )
    await send_playlist_to_user(msg=msg, 
                                playlist=playlist)


@messages_router.message(CommandStart())
async def start_cmd_handler(msg: Message, 
                            state: FSMContext):
    user = UserScheme(telegram_user_id=msg.from_user.id, 
                      nickname=msg.from_user.username)
    user_service.create_user(user=user)
    
    answer = ("📖 Краткий экскурс:\n\n" \
              "/new — создание нового плейлиста\n" \
              "/playlists — ваши плейлисты\n" \
              "/help — помощь\n" \
              "/start — перезапуск бота\n")
    
    await msg.answer(text=answer)
    await state.clear()


@messages_router.message(Command("new"))
async def start_cmd_handler(msg: Message, 
                            state: FSMContext):
    answer = ("⚡️ Итак, вы решили создать плейлист\n\n" \
              "👑 Отправьте его название в чат")
    await msg.answer(text=answer)
    
    await state.set_state(
        states.CreatePlaylistStatesGroup.set_name
    )


@messages_router.message(states.CreatePlaylistStatesGroup.set_name)
async def start_cmd_handler(msg: Message, 
                            state: FSMContext):
    state_data = {
        "playlist_name": msg.text
    }
    await state.update_data(data=state_data)
    
    answer = ("📸 Отправь мне обложку плейлиста")
    await msg.answer(text=answer)
    
    await state.set_state(
        states.CreatePlaylistStatesGroup.set_preview
    )
    
    
@messages_router.message(F.photo, 
                         states.CreatePlaylistStatesGroup.set_preview)
async def start_cmd_handler(msg: Message, 
                            state: FSMContext):
    state_data = {
        "playlist_preview_file_id": msg.photo[-1].file_id
    }
    await state.update_data(data=state_data)
    
    answer = ("ℹ️ Добавь описание плейлисту")
    await msg.answer(text=answer)
    
    await state.set_state(
        states.CreatePlaylistStatesGroup.set_description
    )

    
@messages_router.message(states.CreatePlaylistStatesGroup.set_description)
async def start_cmd_handler(msg: Message, 
                            state: FSMContext):
    state_data = await state.get_data()
    
    playlist = PlaylistScheme(
        creator_telegram_id=msg.from_user.id,
        preview_file_id=state_data.get("playlist_preview_file_id"), 
        name=state_data.get("playlist_name"), 
        description=msg.text
    )
    playlist_service.create_playlist(playlist=playlist)
    
    await send_playlist_to_user(msg=msg, 
                                playlist=playlist)
    
    answer = ("✅ Прекрасно, плейлист создан. " \
              "Чтобы добавить в него музыку – просто " \
              "перешли её мне и выбери плейлист, " \
              "в который её нужно добавить")
    await msg.answer(text=answer)
    
    await state.clear()


@messages_router.message(Command("playlists"))
async def start_cmd_handler(msg: Message, 
                            state: FSMContext):
    answer = "🎧 Ваши плейлисты\n\n"
    
    playlists = playlist_service.get_user_playlists(
        msg.from_user.id
    )
    bot_data = await bot.get_me()
    bot_username = bot_data.username
    
    for playlist in playlists:
        playlist_url = f"https://t.me/{bot_username}?start=playlist_{playlist.pk}"
        answer += (f"<a href='{playlist_url}'>" \
                   f"▶️ {playlist.name}" \
                   f"</a> ({playlist.description})\n\n")
    
    await msg.answer(text=answer)
    
    await state.clear()
    
    

@messages_router.message(F.audio)
async def save_song_to_playlist(msg: Message, 
                            state: FSMContext):
    playlists = playlist_service.get_user_playlists(
        msg.from_user.id
    )
    reply_markup = keyboards.get_playlist_reply_markup(
        playlists=playlists
    )
    
    answer = ("▶️ В какой плейлист сохранить?")
    await msg.answer(text=answer, 
                     reply_markup=reply_markup)
    
    await state.set_state(
        states.PlaylistSongStatesGroup.select_save_playlist
    )
    
    state_data = {
        "audio_file_id": msg.audio.file_id
    }
    
    await state.update_data(
        data=state_data
    )
    