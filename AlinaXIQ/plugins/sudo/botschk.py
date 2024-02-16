import random
from pyrogram import filters
from AlinaXIQ import app
from AlinaXIQ import *
from ... import *
import config

from ...logging import LOGGER

from AlinaXIQ import app, userbot
from AlinaXIQ.core.userbot import *

import asyncio

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import OWNER_ID

import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from dotenv import load_dotenv
from AlinaXIQ.core.userbot import Userbot
from datetime import datetime

# Assuming Userbot is defined elsewhere
userbot = Userbot()


BOT_LIST = ["IQJOBOT", "IQMCBOT", "IQDLBOT", "IQDNBOT", "IQIDBOT"]

@app.on_message(filters.command(["botschk","چالاکی بۆت","بۆتەکانم","botchk"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]))
async def bots_chk(_, message):
    msg = await message.reply_video(video="https://graph.org/file/126924df745817ea5e511.mp4", caption="**پشکنین بۆ بۆتەکانم چالاکن یان ناچالاك👾🚀!**")
    response = "**پشکنین بۆ بۆتەکانم چالاکن یان ناچالاك👾🚀!**\n\n"
    for bot_username in BOT_LIST:
        try:
            bot = await app.get_users(bot_username)
            bot_id = bot.id
            await asyncio.sleep(0.5)
            bot_info = await app.send_message(bot_id, "/start")
            await asyncio.sleep(3)
            async for bot_message in app.get_chat_history(bot_id, limit=1):
                if bot_message.from_user.id == bot_id:
                    response += f"**╭⎋ [{bot.first_name}](tg://user?id={bot.id})\n╰⊚ دۆخ: چالاك ✅**\n\n"
                else:
                    response += f"**╭⎋ [{bot.first_name}](tg://user?id={bot.id})\n╰⊚ دۆخ: ناچالاك ❌**\n\n"
        except Exception:
            response += f"**╭⎋ {bot_username}\n╰⊚ دۆخ: هەڵە ❌**\n"
    
    await msg.edit_text(response)
                
