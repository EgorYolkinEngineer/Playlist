from aiogram.types import BotCommand

from src.handlers.messages import messages_router 
from src.handlers.inline_query import inline_router
from src.handlers.callback_query import callback_query_router

from core.conf.config import bot, dp

import asyncio

dp.include_routers(messages_router,
                   callback_query_router,
                   inline_router)


async def set_default_commands(dp):
    await bot.set_my_commands(
        [
            BotCommand(
                command='new', 
                description='Create new playlist'
            ), 
            BotCommand(
                command='playlists', 
                description='Show your playlists'
            ), 
            BotCommand(
                command='help', 
                description='Help message'
            ),
            BotCommand(
                command='start', 
                description='Run bot'
            )
        ]
    )


async def start(dispatcher) -> None:
    bot_name = dict(await bot.get_me()).get('username')
    await set_default_commands(dispatcher)
    print(f'#    start on @{bot_name}')


async def end(dispatcher) -> None:
    bot_name = dict(await bot.get_me()).get('username')
    print(f'#    end on @{bot_name}')


async def main():
    await start(dispatcher=dp)
    await dp.start_polling(bot)
    await end(dispatcher=dp)
    