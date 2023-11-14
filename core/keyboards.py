from aiogram.types import (InlineKeyboardButton, 
                           InlineKeyboardMarkup, 
                           SwitchInlineQueryChosenChat)

from core.conf.config import bot
from core.schemas import PlaylistScheme


def get_share_playlist_reply_markup(playlist: PlaylistScheme, 
                                    delete_button: bool = False
                                    ) -> InlineKeyboardMarkup:
    """ Get Share button. """
    
    switch_chat = SwitchInlineQueryChosenChat(query=playlist.name, 
                                              allow_user_chats=True, 
                                              allow_group_chats=True, 
                                              allow_channel_chats=True)
    
    inline_keyboard = [
        [
            InlineKeyboardButton(text="Поделиться 🔗", 
                                switch_inline_query_chosen_chat=switch_chat)
        ]
    ]
    
    if delete_button:
        inline_keyboard[0].append(
            InlineKeyboardButton(text="Удалить 🗑️", 
                                 callback_data=f"delete_playlist_{playlist.pk}")
        )
    
    
    reply_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return reply_markup


async def get_listen_playlist_reply_markup(playlist_pk: int
                                           ) -> InlineKeyboardMarkup:
    """ Get Listen button. """
    
    bot_data = await bot.get_me()
    bot_username = bot_data.username
    reply_markup_url = f"https://t.me/{bot_username}?start=playlist_{playlist_pk}"
    
    reply_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Прослушать 🎧", 
                                 url=reply_markup_url)
        ]
    ])
    return reply_markup


def get_playlist_reply_markup(playlists: list[PlaylistScheme]
                              ) -> InlineKeyboardMarkup:
    """ Get playlists keyboard. """
    
    inline_keyboard = list()
    
    for playlist in playlists:
        inline_keyboard.append([
            InlineKeyboardButton(text=playlist.name, 
                                 callback_data=str(playlist.pk))
        ])

    reply_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return reply_markup