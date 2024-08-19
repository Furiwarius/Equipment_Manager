from app.settings.settings import db_log_setting

import asyncio
from aiogram import Bot, Dispatcher


class TelegramClient():

    def __init__(self) -> None:
        
        # Объект бота
        self.bot = Bot(token=db_log_setting.TELEGRAM_API_TOKEN)
        # Диспетчер
        self.dp = Dispatcher()



    async def _send(self, message:str):
        await self.bot.send_message(db_log_setting.DEVELOPER_USER_ID, message)
        await self.bot.session.close()



    def send(self, message:str):
        asyncio.run(self._send(message))