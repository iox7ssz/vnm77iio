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




@app.on_message(command(["/addbots", "زیادکردنی بۆت", "/addbot", f"/addbots@{app.username}"]) & SUDOERS)
async def add_all(client, message):
    
    done = 0
    failed = 0
    lol = await message.reply("**✅┋ زیادکردنی بۆت لە هەموو گرووپەکان**")
    try:
        userbot = await get_assistant(message.chat.id)
        async for dialog in userbot.get_dialogs():
            if dialog.chat.id == -1001962701094:
                continue
            try:
                await userbot.add_chat_members(dialog.chat.id, app.id)
                done += 1
                await lol.edit(
                    message.chat.id,
                    f"**✅┋ یاریدەدەر بۆتی زیادکرد بۆ {done} گرووپ**"
                )
            except Exception as e:
                failed += 1
                await lol.edit(
                    message.chat.id,
                    f"**❌┋ شکستی هێنا لە زیادکردنی بۆت**"
                )
            await asyncio.sleep(1)  # Adjust sleep time based on rate limits
    finally:
        await lol.edit(
            message.chat.id,
            f"**✅┋ زیادکرا بۆ : {done} گرووپ\n❌┋ شکستی هێنا لە : {failed} گرووپ**"
        )
