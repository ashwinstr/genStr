# config.py
import os


class Config:

    API_HASH = os.environ.get("API_HASH")
    API_ID = int(os.environ.get("API_ID"))
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    CMD_TRIGGER = os.environ.get("CMD_TRIGGER")
    LOG_CHANNEL_ID = int(os.environ.get("LOG_CHANNEL_ID"))
    OWNER_ID = int(os.environ.get("OWNER_ID", 0))
