from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import (Bot, Dispatcher)

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    TELEGRAM_API_KEY: str
    
    
config = Config(_env_file="./.env")

bot = Bot(token=config.TELEGRAM_API_KEY, 
          parse_mode="HTML")
dp = Dispatcher(bot=bot, 
                storage=MemoryStorage())
