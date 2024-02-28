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
from strings.filters import command
from AlinaXIQ.utils.alina_ban import admin_filter
from AlinaXIQ.utils.decorators.userbotjoin import UserbotWrapper
from AlinaXIQ.utils.database import get_assistant

links = {}


@app.on_message(command(
    ["/userbotjoin", f"userbotjoin@{app.username}", "زیادکردنی یاریدەدەر", f"جۆین@{app.username}"]) & ~filters.private)
async def join_group(client, message):
    chat_id = message.chat.id
    userbot = await get_assistant(message.chat.id)

    if message.chat.username:
        try:
            await userbot.join_chat(message.chat.username)
            await message.reply("**✅┋ بە سەرکەوتوویی ئەکاونتی یاریدەدەر جۆین بوو**")
        except ChatAdminRequired:
            await message.reply_text("**✅┋ بمکە ئەدمین بۆ ئەوەی بتوانم بانگهێشتی بکەم**")
            return
        except UserNotParticipant:
            member = await app.get_chat_member(chat_id, userbot.id)
            if member.status in (ChatMemberStatus.BANNED, ChatMemberStatus.RESTRICTED):
                try:
                    await app.unban_chat_member(chat_id, userbot.id)
                except Exception as e:
                    await message.reply("**❌┋ ئەکاونتی یاریدەدەر باندکراوە باندەکەی لابە سەرەتا**")
                    return
                invite_link = await app.create_chat_invite_link(chat_id)
                await userbot.join_chat(invite_link.invite_link)
                await message.reply(
                    "**❌┋ ئەکاونتی یاریدەدەر باندکراوە باندەکەی لابە سەرەتا دواتر فەرمان دووبارە بکەوە**")
            else:
                await message.reply("**❌┋ ئەکاونتی یاریدەدەر باندکراوە باندەکەی لابە سەرەتا**")
    else:
        try:
            member = await app.get_chat_member(chat_id, userbot.id)
            if member.status in (ChatMemberStatus.BANNED, ChatMemberStatus.RESTRICTED):
                try:
                    await app.unban_chat_member(chat_id, userbot.id)
                    invite_link = await app.create_chat_invite_link(chat_id)
                    await userbot.join_chat(invite_link.invite_link)
                    await message.reply(
                        "**❌┋ ئەکاونتی یاریدەدەر باندکراوە باندەکەی لابە سەرەتا دواتر فەرمان دووبارە بکەوە**")
                except Exception as e:
                    await message.reply("**❌┋ ئەکاونتی یاریدەدەر باندکراوە باندەکەی لابە سەرەتا**")
                    return
                invite_link = await app.create_chat_invite_link(chat_id)
                await userbot.join_chat(invite_link.invite_link)
                await message.reply(
                    "**❌┋ ئەکاونتی یاریدەدەر باندکراوە باندەکەی لابە سەرەتا دواتر فەرمان دووبارە بکەوە**")
            else:
                await message.reply("**ئەکاونتی یاریدەدەر لە گرووپە**")
        except ChatAdminRequired:
            await message.reply("**❌┋ ببورە من ئەدمین نیم**")


@app.on_message(command(["/userbotleave", "دەرکردنی یاریدەدەر", "/assleft"]) & ~filters.private & admin_filter)
async def leave_one(client, message):
    try:
        userbot = await get_assistant(message.chat.id)
        await userbot.leave_chat(message.chat.id)
        await app.send_message(message.chat.id, "**✅┋ بە سەرکەوتوویی ئەکاونتی یاریدەدەر لێفتی کرد**")
    except Exception as e:
        print(e)


@app.on_message(command(["لێفتی گشتی", f"/leaveall@{app.username}", f"لێفت@{app.username}"]) & SUDOERS)
async def leave_all(client, message):
    if message.from_user.id not in SUDOERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("✅┋ ئەکاونتی یاریدەدەری بۆت لێفت دەکات لە هەموو گرووپەکان")
    try:
        userbot = await get_assistant(message.chat.id)
        async for dialog in userbot.one.get_dialogs():
            if dialog.chat.id == -1001962701094:
                continue
            try:
                await userbot.leave_chat(dialog.chat.id)
                left += 1
                await lol.edit(
                    f"**✅┋ لێفت دەکات لە هەموو گرووپەکان . .\n\n✅┋ لێفت دەکات : {left} گرووپ\n❌┋ شکستی هێنا لە : {failed} گرووپ**"
                )
            except BaseException:
                failed += 1
                await lol.edit(
                    f"**✅┋ لێفت دەکات . .\n\n✅┋ لێفت دەکات لە : {left} گرووپ\n❌┋ شکستی هێنا لە : {failed} گرووپ**"
                )
            await asyncio.sleep(3)
    finally:
        await app.send_message(
            message.chat.id, f"**✅┋ لێفتی کرد لە : {left} گرووپ\n❌┋ شکستی هێنا لە : {failed} گرووپ**"
        )
