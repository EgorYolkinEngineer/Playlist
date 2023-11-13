from pydantic_settings import BaseSettings


from aiogram import (Bot, 
                     Dispatcher)


class Config(BaseSettings):
    TELEGRAM_API_KEY: str
    
    
config = Config(_env_file=".env")

bot = Bot(token=config.TELEGRAM_API_KEY)
dp = Dispatcher(bot=bot)
