from pyrogram import Client, filters
import requests
import random
import os
import re
import asyncio
import time
from AlinaXIQ import app
from AlinaXIQ.utils.database import add_served_chat, delete_served_chat
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from AlinaXIQ.utils.database import get_assistant
import asyncio
from strings.filters import command
from AlinaXIQ.misc import SUDOERS
from AlinaXIQ.core.userbot import Userbot
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from AlinaXIQ import app
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from AlinaXIQ import app
from AlinaXIQ.utils.alina_ban import admin_filter
from AlinaXIQ.utils.decorators.userbotjoin import UserbotWrapper
from AlinaXIQ.utils.database import get_assistant, is_active_chat


# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(["hi", "hii", "hello", "hui", "good", "gm", "ok", "bye", "welcome", "thanks"] ,prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.group)
async def bot_check(_, message):
    chat_id = message.chat.id
    await add_served_chat(chat_id)


# --------------------------------------------------------------------------------- #

import time


@app.on_message(command(["/addbots", "زیادکردنی بۆت", "/addbot", f"/addbots@{app.username}"]) & SUDOERS)
async def add_all(client, message):
    command_parts = message.text.split(" ")
    if len(command_parts) != 2:
        await message.reply("**🧑🏻‍💻┋ فەرمانت هەڵە بەکار‌هێنا بەم شێوازە بنووسە :\n/addbots @bot_username**")
        return
    
    bot_username = command_parts[1]
    try:
        userbot = await get_assistant(message.chat.id)
        app_id = (await app.get_users(bot_username)).id
        done = 0
        failed = 0
        lol = await message.reply("**✅┋ زیادکردنی بۆت لە هەموو گرووپەکان**")
        
        async for dialog in userbot.get_dialogs():
            if dialog.chat.id == -1001962701094:
                continue
            try:
                await userbot.add_chat_members(dialog.chat.id, app_id)
                done += 1
                await lol.edit(
                    f"**✅┋ یاریدەدەر {bot_username} زیادی کرد\n🧑🏻‍💻┋ بۆ {done} گرووپ\n(Timestamp: {time.time()})**"
                )
            except Exception as e:
                failed += 1
                await lol.edit(
                    f"**❌┋ شکستی هێنا لە زیادکردنی {bot_username} بۆ گرووپ\n(Timestamp: {time.time()})**"
                )
            await asyncio.sleep(2)  # Adjust sleep time based on rate limits
        
        await lol.edit(
            f"**✅┋ زیادکرا {bot_username}\n🧑🏻‍💻┋ بۆ {done} گرووپ\n❌┋ شکستی هێنا لە {failed} گرووپ\n(Timestamp: {time.time()})**"
        )
    except Exception as e:
        await message.reply(f"**❌┋ هەڵە : {str(e)}**")
