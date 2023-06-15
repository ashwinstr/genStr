import os
import json
import time
import asyncio

from bot import Bot, Config
from pyromod import listen
from asyncio.exceptions import TimeoutError

from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    SessionPasswordNeeded, FloodWait,
    PhoneNumberInvalid, ApiIdInvalid,
    PhoneCodeInvalid, PhoneCodeExpired
)

bot = Bot()

API_TEXT = """Hi {}
Welcome to pyrogram's `HU_STRING_SESSION` generator bot.

`Send your API_ID to Continue.`"""
HASH_TEXT = "`Send your API_HASH to Continue.`\n\nPress /cancel to Cancel."
PHONE_NUMBER_TEXT = (
    "`Now send your phone number to continue...`\n"
    "**Note:** Include Country code. eg. +13124562345\n\n"
    "Press /cancel to cancel."
)


@bot.on_message(filters.private & filters.command("start"))
async def genStr(bot: Bot, msg: Message):
    chat = msg.chat
    api = await bot.ask(
        chat.id, API_TEXT.format(msg.from_user.mention)
    )
    if await is_cancel(msg, api.text):
        return
    try:
        int(api.text)
    except Exception:
        await api.delete()
        await msg.reply("`API ID Invalid.`\nPress /start to create again.")
        return
    api_id = api.text
    await api.delete()
    hash = await bot.ask(chat.id, HASH_TEXT)
    if await is_cancel(msg, hash.text):
        return
    api_hash = hash.text
    await hash.delete()
    try:
        client = Client("my_account", api_id=api_id, api_hash=api_hash)
    except Exception as e:
        await bot.send_message(chat.id ,f"**ERROR:** `{str(e)}`\nPress /start to create again.")
        return
    try:
        await client.connect()
    except ConnectionError:
        await client.disconnect()
        await client.connect()
    await msg.reply("`Successfully connected to you client.`")
    while True:
        number = await bot.ask(chat.id, PHONE_NUMBER_TEXT)
        if not number.text:
            continue
        if await is_cancel(msg, number.text):
            await client.disconnect()
            return
        phone = number.text
        await number.delete()
        confirm = await bot.ask(chat.id, f'`Is "{phone}" correct? (y/n):`\n\nType: `y` (if yes)\nType: `n` (if no)')
        if await is_cancel(msg, confirm.text):
            await client.disconnect()
            return
        if "y" in confirm.text.lower():
            await confirm.delete()
            break
    try:
        code = await client.send_code(phone)
        await asyncio.sleep(1)
    except FloodWait as e:
        await msg.reply(f"`You have floodwait of {e.x} seconds`")
        return await bot.sleep(msg)
    except ApiIdInvalid:
        await msg.reply("`API_ID and API_HASH are invalid.`\n\nPress /start to create again.")
        return await bot.sleep(msg)
    except PhoneNumberInvalid:
        await msg.reply("`Your phone number is invalid.`\n\nPress /start to create again.")
        return await bot.sleep(msg)
    try:
        otp = await bot.ask(
            chat.id, ("`An otp is sent to your phone number.`\n"
                      "Please enter otp in `1 2 3 4 5` format.\n\n"
                      "`If bot not sending OTP then try` /restart `cmd and again` /start `the Bot.`\n"
                      "Press /cancel to cancel."), timeout=300)
    except TimeoutError:
        await msg.reply("`Time limit reached of 5 min.\nPress /start to create again.`")
        return await bot.sleep(msg)
    if await is_cancel(msg, otp.text):
        return await client.disconnect()
    otp_code = otp.text
    await otp.delete()
    try:
        await client.sign_in(phone, code.phone_code_hash, phone_code=' '.join(str(otp_code)))
    except PhoneCodeInvalid:
        await msg.reply("`Invalid code.`\n\nPress /start to create again.")
        return await bot.sleep(msg)
    except PhoneCodeExpired:
        await msg.reply("`Code is expired.`\n\nPress /start to create again.")
        return await bot.sleep(msg)
    except SessionPasswordNeeded:
        try:
            two_step_code = await bot.ask(
                chat.id, 
                "`This account have two-step verification code.\nPlease enter your second factor authentication code.`\nPress /cancel to Cancel.",
                timeout=300
            )
        except TimeoutError:
            await msg.reply("`Time limit reached of 5 min.\n\nPress /start to create again.`")
            return await bot.sleep(msg)
        if await is_cancel(msg, two_step_code.text):
            return await client.disconnect()
        new_code = two_step_code.text
        await two_step_code.delete()
        try:
            await client.check_password(new_code)
        except Exception as e:
            await msg.reply(f"**ERROR:** `{str(e)}`")
            return await bot.sleep(msg)
    except Exception as e:
        await bot.send_message(chat.id, f"**ERROR:** `{str(e)}`")
        return await bot.sleep(msg)
    session_string = await client.export_session_string()
    await client.send_message("me", f"#PYROGRAM #HU_STRING_SESSION #UX_xplugin_support\n\n```{session_string}```")

    text = "`String session is successfully generated.\nClick on button Below.`"
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Click Me", url=f"tg://openmessage?user_id={chat.id}")]]
    )
    await bot.send_message(chat.id, text, reply_markup=reply_markup)
    return await bot.sleep(msg)


@bot.on_message(filters.private & filters.command("restart"))
async def restart(bot: Bot, msg: Message):
    if msg.from_user.id == 1013414037:
        await msg.reply('✅')
        await bot.restart()


@bot.on_message(filters.private & filters.command("help"))
async def start(_, msg: Message):
    out = f"""
Hello {msg.from_user.mention}, this is pyrogram session string generator bot which gives you `HU_STRING_SESSION` for your userbot.

It needs `API_ID` , `API_HASH` , `PHONE_NUMBER` and `One time Verification Code` which will be sent to your `PHONE_NUMBER`.
You have to put `OTP` in `1 2 3 4 5` format.

**NOTE:** `If bot not sending OTP to your PHONE_NUMBER then try` /restart `command and again` /start `your process.`

(C) Author: [Krishna Singhal](https://t.me/Krishna_Singhal) and
[UsergeTeam](https://t.me/TheUserge)

**Forked by:** [Kakashi](https://t.me/Kakashi_HTK)
**Support group:** [UX_xplugin_support](https://t.me/UX_xplugin_support)
Give a star ⭐️ to [Author REPO](https://github.com/Krishna-Singhal/genStr) and [Forked REPO](https://github.com/ashwinst\
r/genStr) if you like this bot.
"""
    await msg.reply(out, disable_web_page_preview=True)


async def is_cancel(msg: Message, text: str):
    if text.startswith("/cancel"):
        await msg.reply("`Process cancelled.`")
        return True
    return False


if __name__ == "__main__":
    bot.run()
