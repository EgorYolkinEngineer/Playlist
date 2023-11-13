from aiogram.types import Message
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import FSInputFile

import asyncio, os

from core.conf.config import bot
from core.conf import config
 
from core.services.user_service import user_service
from core.schemas import (UserScheme, 
                          PlaylistScheme, 
                          PlaylistSongScheme)

messages_router = Router(name="messages")


@messages_router.message(CommandStart())
async def start_cmd_handler(msg: Message):
    user = UserScheme(telegram_user_id=msg.from_user.id, 
                      nickname=msg.from_user.username)
    user_service.create_user(user=user)
    
    await msg.answer(text=msg.text)
