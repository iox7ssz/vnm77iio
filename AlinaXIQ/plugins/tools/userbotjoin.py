import asyncio
from AlinaXIQ.misc import SUDOERS
from AlinaXIQ.core.userbot import Userbot
from pyrogram import Client, filters
from strings.filters import command
from pyrogram.errors import UserAlreadyParticipant
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
links = {}


@app.on_message(command(["/userbotjoin", f"userbotjoin@{app.username}", "زیادکردنی یاریدەدەر", f"جۆین@{app.username}"]) & ~filters.private)
async def join_group(client, message):
    chat_id = message.chat.id
    userbot = await get_assistant(message.chat.id)
    done = await message.reply("**✅┋ کەمێك چاوەڕێ بکە بانگهێشت دەکرێت . .**") 
    # Get chat member object
    chat_member = await app.get_chat_member(chat_id, app.id)
    
    # Condition 1: Group username is present, bot is not admin
    if message.chat.username and not chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        try:
            await userbot.join_chat(message.chat.username)
            await done.edit_text("**✅┋ بە سەرکەوتوویی ئەکاونتی یاریدەدەر جۆین بوو**")
        except ChatAdminRequired:
            await done.edit_text("**✅┋ ڕۆڵی باندم مێبدە بۆ ئەوەی بتوانم باندی لابەم**")
            

    # Condition 2: Group username is present, bot is admin, and Userbot is not banned
    if message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        try:
            invite_link = await app.create_chat_invite_link(chat_id, expire_date=None)
            await userbot.join_chat(invite_link.invite_link)
            await done.edit_text("**✅┋ بە سەرکەوتوویی ئەکاونتی یاریدەدەر جۆین بوو**")
        except Exception as e:
            await done.edit_text(str(e))

    
    
    # Condition 3: Group username is not present/group is private, bot is admin and Userbot is banned
    if message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        userbot_member = await app.get_chat_member(chat_id, userbot.id)
        if userbot_member.status in [ChatMemberStatus.BANNED, ChatMemberStatus.RESTRICTED]:
            try:
                await app.unban_chat_member(chat_id, userbot.id)
                await done.edit_text("**✅┋ ئەکاونتی یاریدەدەر باندی لادرا**")
                await userbot.join_chat(message.chat.username)
                await done.edit_text("**❌┋ ئەکاونتی یاریدەدەر باندکراوە باندەکەی لابە سەرەتا دواتر فەرمان دووبارە بکەوە**")
            except Exception as e:
                await done.edit_text("**❌┋ شکستی هێنا لە جۆین کردن تکایە ڕۆڵی باند و بانگکردنی کەسەکانم پێبە**")
        return
    
    # Condition 4: Group username is not present/group is private, bot is not admin
    if not message.chat.username and not chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        await done.edit_text("**✅┋ بمکە ئەدمین بۆ ئەوەی بتوانم بانگهێشتی بکەم**")
        


    # Condition 5: Group username is not present/group is private, bot is admin
    if not message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        try:
            invite_link = await app.create_chat_invite_link(chat_id, expire_date=None)
            await userbot.join_chat(invite_link.invite_link)
            await message.reply("**✅┋ بە سەرکەوتوویی ئەکاونتی یاریدەدەر جۆین بوو**")
        except Exception as e:
            await message.reply(str(e))

    
    
    # Condition 6: Group username is not present/group is private, bot is admin and Userbot is banned
    if not message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        userbot_member = await app.get_chat_member(chat_id, userbot.id)
        if userbot_member.status in [ChatMemberStatus.BANNED, ChatMemberStatus.RESTRICTED]:
            try:
                await app.unban_chat_member(chat_id, userbot.id)
                await done.edit_text("**✅┋ ئەکاونتی یاریدەدەر باندی لادرا\n\n✅┋ بنووسە : /userbotjoin **")
                invite_link = await app.create_chat_invite_link(chat_id, expire_date=None)
                await userbot.join_chat(invite_link.invite_link)
                await done.edit_text("**❌┋ ئەکاونتی یاریدەدەر باندکراوە باندەکەی لابە سەرەتا دواتر فەرمان دووبارە بکەوە**")
            except Exception as e:
                await message.reply(str(e))
        return
        
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
