# config.py

import os
import dotenv

if os.path.isfile("config.env"):
    dotenv.load_dotenv("config.env")


class Config:

    API_HASH = os.environ.get("API_HASH")
    API_ID = int(os.environ.get("API_ID", 0))
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    CMD_TRIGGER = os.environ.get("CMD_TRIGGER")
    LOG_CHANNEL_ID = int(os.environ.get("LOG_CHANNEL_ID", 0))
    OWNER_ID = int(os.environ.get("OWNER_ID", 0))
