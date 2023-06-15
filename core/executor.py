# executor for maintenance purpose
from pyrogram import filters
from pyrogram.types import Message

from core.genStr import bot
from helpers.config import Config


@bot.on_message(
    filters.user([Config.OWNER_ID])
    & filters.command("eval", prefixes=[Config.CMD_TRIGGER]),
    group=-2
)
async def evaluator(_, message: Message):
    """ code evaluator """
    text = " ".join(message.text.split()[:-1]) if message.text else None
    if not text:
        return await message.reply("`Text not found...\nGive input to run commands.`")
    try:
        evaluated = eval(text)
        await message.reply(evaluated)
    except Exception as e:
        await bot.send_message(Config.LOG_CHANNEL_ID, str(e))
