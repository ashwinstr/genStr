import os
from dotenv import load_dotenv

from pyrogram import Client
from pyrogram.types import Message
from pyromod import listen


if os.path.isfile("config.env"):
    load_dotenv("config.env")


class Config:
    API_ID = int(os.environ.get("API_ID", 0))
    API_HASH = os.environ.get("API_HASH", None)
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    LOG_CHANNEL_ID = int(os.environ.get("LOG_CHANNEL_ID", 0))


class Bot(Client):
    def __init__(self):
        kwargs = {
            'name': 'session_bot',
            'in_memory': True,
            'api_id': Config.API_ID,
            'api_hash': Config.API_HASH,
            'bot_token': Config.BOT_TOKEN
        }
        super().__init__(**kwargs)

    async def start(self):
        await super().start()
        await self.send_message(Config.LOG_CHANNEL_ID, "`Started session string bot successfully...`")
        print("Bot has been started...")

    async def stop(self, block: bool = True):
        await super().stop()

    async def sleep(
        self: 'Client',
        msg: Message,
        block: bool = True
    ):
        await msg.reply("`Sleeping for 10 seconds.`")
        await super().restart(block)
