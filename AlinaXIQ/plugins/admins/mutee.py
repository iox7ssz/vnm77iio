import asyncio
from AlinaXIQ import app
from datetime import datetime
from pyrogram.enums import ChatMembersFilter
from pyrogram.enums import ChatMemberStatus
from pyrogram import enums
from pyrogram.types import (InlineKeyboardButton, ChatPermissions, InlineKeyboardMarkup, Message, User)
from pyrogram import Client, filters
from AlinaXIQ import (Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app)
import sys
from pyrogram.types import ChatPermissions, ChatPrivileges
from pyrogram.errors import PeerIdInvalid
from os import getenv
from AlinaXIQ.misc import SUDOERS

unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)

mute_permission = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False, 
    can_send_other_messages=False,
    can_send_polls=False,
    can_add_web_page_previews=False,
    can_change_info=False,
    can_pin_messages=False,
    can_invite_users=True,
)

muted_users = []
@app.on_message(filters.command(["ئاگاداری","میوت"], ""), group=39)
async def mute_user(client, message):
    global muted_users    
    chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
    usr = await client.get_chat(message.from_user.id)
    name = usr.first_name
    get = await client.get_chat_member(message.chat.id, message.from_user.id)
    if get.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or message.from_user.id in SUDOERS:    
        if message.reply_to_message.from_user.id == 833360381:
            await app.send_message(message.chat.id, "**من ناتوانم گەشەپێدەر میوت بکەم بەجدیتە؟😂🙂**")
        else: 
         if message.reply_to_message:
           user_id = message.reply_to_message.from_user.mention
         if user_id not in muted_users:
            muted_users.append(user_id)
            await message.reply_text(f"**{user_id}\nمیوت کرا ༄**")
         else:
           await message.reply_text(f"**{user_id}\nپێشتر میوت کراوە ༄**")
    else:
        await message.reply_text(f"**ئەم فەرمانە بۆ تۆ نییە ༄**")


@app.on_message(filters.command(["لادانی میوت","لادانی ئاگاداری"], ""), group=62)
async def unmute_user(client, message):
   global muted_users
   get = await client.get_chat_member(message.chat.id, message.from_user.id)
   if get.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or message.from_user.id in SUDOERS: 
    user_id = message.reply_to_message.from_user.mention
    if user_id in muted_users:
        muted_users.remove(user_id)
        await message.reply_text(f"**{user_id}\nمیوتی لادرا ༄**")
   else:
        await message.reply_text(f"**ئەم فەرمانە بۆ تۆ نییە ༄**")    
       
        
        
       
@app.on_message(filters.text)
async def handle_message(client, message):
    if message.from_user and message.from_user.id in muted_users:
        await client.delete_messages(chat_id=message.chat.id, message_ids=message.id)

@app.on_message(filters.command(["میوتکراوەکان"], ""), group=137)
async def get_rmuted_users(client, message):
    global muted_users
    usr = await client.get_chat(message.from_user.id)
    name = usr.first_name
    get = await client.get_chat_member(message.chat.id, message.from_user.id)
    if get.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or message.from_user.id in SUDOERS:
         count = len(muted_users)
         user_ids = [str(user) for user in muted_users]
         response = f"**لیستی میوتکراوەکان ژمارەیان : {count}\n**"
         response += "**⭓━⭓⭓⭓⭓━⭓\n**"
         response += "**\n**".join(user_ids)
         await message.reply_text(response)
    else:
        await message.reply_text(f"**ئەم فەرمانە بۆ تۆ نییە ༄**")



@app.on_message(filters.command(["سڕینەوەی میوتکراوەکان"], ""), group=136)
async def unmute_all(client, message):
   usr = await client.get_chat(message.from_user.id)
   name = usr.first_name
   get = await client.get_chat_member(message.chat.id, message.from_user.id)
   if get.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or message.from_user.id in SUDOERS:
    global muted_users
    count = len(muted_users)
    chat_id = message.chat.id
    failed_count = 0

    for member in muted_users.copy():
        user_id = member
        try:
            muted_users.remove(member)
        except Exception:
            failed_count += 1

    successful_count = count - failed_count

    if successful_count > 0:
        await message.reply_text(f"**{successful_count} لادران میوتکراوەکان ༄**")
    else:
        await message.reply_text("**هیچ بەکارهێنەرێکی میوت کراو نییە ༄**")

    if failed_count > 0:
        await message.reply_text(f"**شکستی هێنا لە لادانی {failed_count}\nمیوتکراوەکان ༄**")
   else:
        await message.reply_text(f"**ئەم فەرمانە بۆ تۆ نییە ༄**")
