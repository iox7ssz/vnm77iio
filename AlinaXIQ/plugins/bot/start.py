import time
from time import time
import asyncio
from pyrogram.errors import UserAlreadyParticipant
import random
from pyrogram.errors import UserNotParticipant
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch
import config
from AlinaXIQ import app
from AlinaXIQ.misc import _boot_
from AlinaXIQ.utils import bot_up_time
from AlinaXIQ.plugins.sudo.sudoers import sudoers_list
from AlinaXIQ.utils.database import get_served_chats, get_served_users, get_sudoers
from AlinaXIQ.utils import bot_sys_stats
from AlinaXIQ.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from AlinaXIQ.utils.decorators.language import LanguageStart
from AlinaXIQ.utils.formatters import get_readable_time
from AlinaXIQ.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string
from AlinaXIQ.utils.database import get_assistant
from time import time
import asyncio
from AlinaXIQ.utils.extraction import extract_user

# Define a dictionary to track the last message timestamp for each user
user_last_message_time = {}
user_command_count = {}
# Define the threshold for command spamming (e.g., 20 commands within 60 seconds)
SPAM_THRESHOLD = 2
SPAM_WINDOW_SECONDS = 5


IQ_PICS = [
"https://graph.org/file/9340f44e4a181b18ac663.jpg",
"https://graph.org/file/50037e072302b4eff55ba.jpg",
"https://graph.org/file/39f39cf6c6c68170f6bf2.jpg",
"https://graph.org/file/abf9931642773bc27ad7f.jpg",
"https://graph.org/file/60764ec9d2b1fda50c2d1.jpg",
"https://graph.org/file/a90c116b776c90d58f5e8.jpg",
"https://graph.org/file/b2822e1b60e62caa43ceb.jpg",
"https://graph.org/file/84998ca9871e231df0897.jpg",
"https://graph.org/file/6c5493fd2f6c403486450.jpg",
"https://graph.org/file/9dd91a4a794f15e5dadb3.jpg",
"https://graph.org/file/0a2fb6e502f6c9b6a04ac.jpg",
"https://graph.org/file/774380facd73524f27d26.jpg"

]

IQ_VIDS = [
"https://telegra.ph/file/79055663111eaa8824b26.mp4",
"https://telegra.ph/file/96b75e112896a00c47203.mp4",
"https://telegra.ph/file/f35b4a68ec793efe46c7c.mp4",
"https://graph.org/file/d55b419cf02dfcdd5a2b8.mp4",
"https://graph.org/file/cfa01d6254cfa3b6fd945.mp4",
"https://telegra.ph/file/b61c1ce580957e936d8fb.mp4",
"https://telegra.ph/file/f2aec19f7387741798fa8.mp4",
"https://telegra.ph/file/e13f1c42b949221f87e77.mp4"

]



@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    user_id = message.from_user.id
    current_time = time()
    # Update the last message timestamp for the user
    last_message_time = user_last_message_time.get(user_id, 0)

    if current_time - last_message_time < SPAM_WINDOW_SECONDS:
        # If less than the spam window time has passed since the last message
        user_last_message_time[user_id] = current_time
        user_command_count[user_id] = user_command_count.get(user_id, 0) + 1
        if user_command_count[user_id] > SPAM_THRESHOLD:
            # Block the user if they exceed the threshold
            hu = await message.reply_text(f"**🧑🏻‍💻┋ {message.from_user.mention} بۆت سپام مەکە بەڕێز\n🧑🏻‍💻┋ پێنج چرکە بوەستە**")
            await asyncio.sleep(3)
            await hu.delete()
            return 
    else:
        # If more than the spam window time has passed, reset the command count and update the message timestamp
        user_command_count[user_id] = 1
        user_last_message_time[user_id] = current_time

    await add_served_user(message.from_user.id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            return await message.reply_photo(
                random.choice(IQ_PICS),
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"**🧑🏻‍💻┋ کەسێکی نوێ هاتە ناو بۆت پشکنینی گەشەپێدەران\n\n👤┋ ناوی : {message.from_user.mention}\n👾┋ یوزەری : @{message.from_user.username}\n🆔┋ ئایدی :** `{message.from_user.id}`",
                )
            return
        if name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                        InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"**🧑🏻‍💻┋ کەسێکی نوێ هاتە ناو بۆت زانیاری گۆرانی\n\n👤┋ ناوی : {message.from_user.mention}\n👾┋ یوزەری : @{message.from_user.username}\n🆔┋ ئایدی :** `{message.from_user.id}`",
                )
    else:
        out = private_panel(_)
        served_chats = len(await get_served_chats())
        served_users = len(await get_served_users())
        UP, CPU, RAM, DISK = await bot_sys_stats()
        await message.reply_photo(
            random.choice(IQ_PICS),
            caption=_["start_2"].format(message.from_user.mention, app.mention, UP, DISK, CPU, RAM,served_users,served_chats),
            reply_markup=InlineKeyboardMarkup(out),
        )
        if await is_on_off(2):
            return await app.send_message(
                chat_id=config.LOGGER_ID,
                text=f"**🧑🏻‍💻┋ کەسێکی نوێ هاتە ناو بۆت\n\n👤┋ ناوی : {message.from_user.mention}\n👾┋ یوزەری : @{message.from_user.username}\n🆔┋ ئایدی :** `{message.from_user.id}`",
            )


    

@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    user_id = message.from_user.id
    current_time = time()
    
    # Update the last message timestamp for the user
    last_message_time = user_last_message_time.get(user_id, 0)

    if current_time - last_message_time < SPAM_WINDOW_SECONDS:
        # If less than the spam window time has passed since the last message
        user_last_message_time[user_id] = current_time
        user_command_count[user_id] = user_command_count.get(user_id, 0) + 1
        if user_command_count[user_id] > SPAM_THRESHOLD:
            # Block the user if they exceed the threshold
            hu = await message.reply_text(f"**🧑🏻‍💻┋ {message.from_user.mention} بۆت سپام مەکە بەڕێز\n🧑🏻‍💻┋ پێنج چرکە بوەستە**")
            await asyncio.sleep(3)
            await hu.delete()
            return 
    else:
        # If more than the spam window time has passed, reset the command count and update the message timestamp
        user_command_count[user_id] = 1
        user_last_message_time[user_id] = current_time
        
    out = start_panel(_)
    BOT_UP = await bot_up_time()
    await message.reply_video(
        random.choice(IQ_VIDS),
        caption=_["start_1"].format(app.mention, BOT_UP),
        reply_markup=InlineKeyboardMarkup(out),
    )
    await add_served_chat(message.chat.id)
    
    # Check if Userbot is already in the group
    try:
        userbot = await get_assistant(message.chat.id)
        message = await message.reply_text(f"**🧑🏻‍💻┋ پشکنین بۆ [یاریدەدەرەکەم](tg://openmessage?user_id={userbot.id}) لە گرووپە یان نا •**")
        is_userbot = await app.get_chat_member(message.chat.id, userbot.id)
        if is_userbot:
            await message.edit_text(f"**🧑🏻‍💻┋ [یاریدەدەرەکەم](tg://openmessage?user_id={userbot.id}) لە گرووپە ئێستا دەتوانی گەڕان بکەیت بۆ گۆرانی •**")
    except Exception as e:
        # Userbot is not in the group, invite it
        try:
            await message.edit_text(f"**🧑🏻‍💻┋ [یاریدەدەرەکەم](tg://openmessage?user_id={userbot.id}) لە گرووپ نییە بانگهێشتی دەکەم ..**")
            invitelink = await app.export_chat_invite_link(message.chat.id)
            await asyncio.sleep(1)
            await userbot.join_chat(invitelink)
            await message.edit_text(f"**🧑🏻‍💻┋ [یاریدەدەرەکەم](tg://openmessage?user_id={userbot.id}) لە گرووپە ئێستا دەتوانی گەڕان بکەیت بۆ گۆرانی •**")
        except Exception as e:
            await message.edit_text(f"**🧑🏻‍💻┋ ناتوانم [یاریدەدەرەکەم](tg://openmessage?user_id={userbot.id}) بانگهێشت بکەم\nبمکە ئەدمین تاوەکو بتوانم زیادی بکەم •**")




@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except Exception as e:
                    print(e)
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    await app.leave_chat(message.chat.id)
                    return
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    await app.leave_chat(message.chat.id)
                    return

                out = start_panel(_)
                chid = message.chat.id
                
                try:
                    userbot = await get_assistant(message.chat.id)
    
                    chid = message.chat.id
                    
                    
                    if message.chat.username:
                        await userbot.join_chat(f"**{message.chat.username}**")
                        await message.reply_text(f"**🧑🏻‍💻┋ [یاریدەدەرەکەم](tg://openmessage?user_id={userbot.id}) هاتە گرووپەوە بەهۆی یوزەری گرووپ •**")
                    else:
                        invitelink = await app.export_chat_invite_link(chid)
                        await asyncio.sleep(1)
                        messages = await message.reply_text(f"**🧑🏻‍💻┋ [یاریدەدەرەکەم](tg://openmessage?user_id={userbot.id}) جۆین دەکات بە بەکارهێنانی لینك •**")
                        await userbot.join_chat(invitelink)
                        await messages.delete()
                        await message.reply_text(f"**🧑🏻‍💻┋ [یاریدەدەرەکەم](tg://openmessage?user_id={userbot.id}) هاتە گرووپەوە بەهۆی لینکی گرووپ •**")
                except Exception as e:
                    await message.edit_text(f"**🧑🏻‍💻┋ تکایە بمکە ئەدمین بۆ بانگهێشت کردنی [یاریدەدەرەکەم](tg://openmessage?user_id={userbot.id}) بۆ گرووپ •**")

                await message.reply_video(
                    random.choice(IQ_VIDS),
                    caption=_["start_3"].format(
                        message.from_user.mentoin,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)
