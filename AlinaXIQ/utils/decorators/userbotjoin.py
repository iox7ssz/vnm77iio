import asyncio

from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters
from AlinaXIQ import YouTube, app
from AlinaXIQ.misc import SUDOERS
from AlinaXIQ.utils.database import (
    get_assistant,
    get_cmode,
    get_lang,
    get_playmode,
    get_playtype,
    is_active_chat,
    is_maintenance,
)
from AlinaXIQ.utils.inline import botplaylist_markup
from config import PLAYLIST_IMG_URL, SUPPORT_CHAT, adminlist
from strings import get_string

links = {}


def UserbotWrapper(command):
    async def wrapper(client, message):
        language = await get_lang(message.chat.id)
        _ = get_string(language)
        
        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    text=f"{app.mention} is under maintenance, visit [support chat]({SUPPORT_CHAT}) for knowing the reason.",
                    disable_web_page_preview=True,
                )

        try:
            await message.delete()
        except:
            pass

        chat_id = message.chat.id

        if not await is_active_chat(chat_id):
            userbot = await get_assistant(chat_id)
            try:
                try:
                    get = await app.get_chat_member(chat_id, userbot.id)
                except ChatAdminRequired:
                    return await message.reply_text("**✅┋ بمکە ئەدمین بۆ ئەوەی بتوانم بانگهێشتی ئەکاونتی یاریدەدەرم بکەم**")
                if (
                    get.status == ChatMemberStatus.BANNED
                    or get.status == ChatMemberStatus.RESTRICTED
                ):
                    return await message.reply_text(
                        _["call_2"].format(
                            app.mention, userbot.id, userbot.name, userbot.username
                        ), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text= "๏ لادانی باند ๏", callback_data=f"unban_assistant")]])
                    )
            except UserNotParticipant:
                if message.chat.username:
                    invitelink = message.chat.username
                    await userbot.join_chat(invitelink)
                else:
                    if chat_id in links:
                        invitelink = links[chat_id]
                        try:
                            await userbot.resolve_peer(invitelink)
                        except:
                            pass
                    else:
                        try:
                            invitelink = await app.export_chat_invite_link(chat_id)
                        except ChatAdminRequired:
                            return await message.reply_text("**✅┋ بمکە ئەدمین بۆ ئەوەی بتوانم بانگهێشتی ئەکاونتی یاریدەدەرم بکەم**")
                        except Exception as e:
                            return await message.reply_text(f"**✅┋ {app.mention} بە سەرکەوتوویی ئەکاونتی یاریدەدەر جۆین بوو\n\n🆔┋ ئایدی : {userbot.mention}..**")

                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
                myu = await message.reply_text("**✅┋ ئەکاونتی یاریدەدەر جۆینی گرووپ دەبێت**")
                try:
                    await asyncio.sleep(1)
                    await userbot.join_chat(invitelink)
                    await myu.delete()
                    await message.reply_text(f"**✅┋ {app.mention} بە سەرکەوتوویی ئەکاونتی یاریدەدەر جۆین بوو\n\n🆔┋ ئایدی : {userbot.mention}..**")
                except InviteRequestSent:
                    try:
                        await app.approve_chat_join_request(chat_id, userbot.id)
                    except Exception as e:
                        return await message.reply_text(
                            _["call_3"].format(app.mention, type(e).__name__)
                        )
                    await asyncio.sleep(3)
                    await myu.delete()
                    await message.reply_text(f"**✅┋ {app.mention} بە سەرکەوتوویی ئەکاونتی یاریدەدەر جۆین بوو\n\n🆔┋ ئایدی : {userbot.mention}..**")
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    return await message.reply_text(f"**✅┋ {app.mention} بە سەرکەوتوویی ئەکاونتی یاریدەدەر جۆین بوو\n\n🆔┋ ئایدی : {userbot.mention}..**")

                links[chat_id] = invitelink

                try:
                    await userbot.resolve_peer(chat_id)
                except:
                    pass

        return await command(client, message, _, chat_id)

    return wrapper
