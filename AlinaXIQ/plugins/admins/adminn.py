import asyncio
from time import time
import re
from pyrogram import Client
from os import getenv
import sys
from AlinaXIQ.misc import SUDOERS
from os import getenv
from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    ChatMemberUpdated,
    ChatPermissions,
    Message,
)

from AlinaXIQ import app
from AlinaXIQ.core.errors import capture_err
from AlinaXIQ.core.keyboard import ikb
from AlinaXIQ.utils.dbfunctions import (
    add_warn,
    get_warn,
    int_to_alpha,
    remove_warns,
    save_filter,
)
from AlinaXIQ.utils.functions import (
    extract_user,
    extract_user_and_reason,
    time_converter,
)


async def member_permissions(chat_id: int, user_id: int):
    perms = []
    try:
        member = await app.get_chat_member(chat_id, user_id)
    except Exception:
        return []
    if member.can_post_messages:
        perms.append("can_post_messages")
    if member.can_edit_messages:
        perms.append("can_edit_messages")
    if member.can_delete_messages:
        perms.append("can_delete_messages")
    if member.can_restrict_members:
        perms.append("can_restrict_members")
    if member.can_promote_members:
        perms.append("can_promote_members")
    if member.can_change_info:
        perms.append("can_change_info")
    if member.can_invite_users:
        perms.append("can_invite_users")
    if member.can_pin_messages:
        perms.append("can_pin_messages")
    if member.can_manage_voice_chats:
        perms.append("can_manage_voice_chats")
    return perms


from AnonXMusic.core.permissions import adminsOnly

admins_in_chat = {}


async def list_admins(chat_id: int):
    global admins_in_chat
    if chat_id in admins_in_chat:
        interval = time() - admins_in_chat[chat_id]["last_updated_at"]
        if interval < 3600:
            return admins_in_chat[chat_id]["data"]

    admins_in_chat[chat_id] = {
        "last_updated_at": time(),
        "data": [
            member.user.id
            async for member in app.get_chat_members(
                chat_id, filter="administrators"
            )
        ],
    }
    return admins_in_chat[chat_id]["data"]


#################

from pyrogram import filters, enums
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ChatPermissions
)
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    UserAdminInvalid,
    BadRequest
)

import datetime
from AlinaXIQ import app


def mention(user, name, mention=True):
    if mention == True:
        link = f"[{name}](tg://openmessage?user_id={user})"
    else:
        link = f"[{name}](https://t.me/{user})"
    return link


async def get_userid_from_username(username):
    try:
        user = await app.get_users(username)
    except:
        return None

    user_obj = [user.id, user.first_name]
    return user_obj


async def ban_user(user_id, first_name, admin_id, admin_name, chat_id, reason, time=None):
    try:
        await app.ban_chat_member(chat_id, user_id)
    except ChatAdminRequired:
        msg_text = "**ڕۆڵی دەرکردنم نییە، ڕۆڵی باندم پێبدە بۆ ئەنجامدانی💘•**"
        return msg_text, False
    except UserAdminInvalid:
        msg_text = "**من ناتوانم ئەدمین دەربکەم بەجدیتە؟😂🙂**"
        return msg_text, False
    except Exception as e:
        if user_id == 833360381:
            msg_text = "**بۆچی دەتەوێ خۆم دەربکەم؟ نا ببورە من وەکو تۆ گەمژەنیم😂🙂!**"
            return msg_text, False

        msg_text = f"**ئۆپسس😂🙂**"
        return msg_text, False

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)

    msg_text += f"**دەرکرا: {user_mention}\nلەلایەن: {admin_mention}**"

    if reason:
        msg_text += f"**هۆکار: `{reason}`\n**"
    if time:
        msg_text += f"**کات: `{time}`\n**"

    return msg_text, True


async def unban_user(user_id, first_name, admin_id, admin_name, chat_id):
    try:
        await app.unban_chat_member(chat_id, user_id)
    except ChatAdminRequired:
        msg_text = "**ڕۆڵی لادانی دەرکردنم نییە، ڕۆڵی باندم پێبدە بۆ ئەنجامدانی💘•**"
        return msg_text
    except Exception as e:
        msg_text = f"**ئۆپسس😂🙂**"
        return msg_text

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)

    msg_text = f"**دەرکردنی لەسەر لادرا: {user_mention}\nلەلایەن: {admin_mention}**"
    return msg_text


async def mute_user(user_id, first_name, admin_id, admin_name, chat_id, reason, time=None):
    try:
        if time:
            mute_end_time = datetime.datetime.now() + time
            await app.restrict_chat_member(chat_id, user_id, ChatPermissions(), mute_end_time)
        else:
            await app.restrict_chat_member(chat_id, user_id, ChatPermissions())
    except ChatAdminRequired:
        msg_text = "**ڕۆڵی میوتکردنم نییە، ڕۆڵی میوتم پێبدە بۆ ئەنجامدانی💘•**"
        return msg_text, False
    except UserAdminInvalid:
        msg_text = "**من ناتوانم ئەدمین میوت بکەم بە جدیتە😂🙂؟**"
        return msg_text, False
    except Exception as e:
        if user_id == 833360381:
            msg_text = "**بۆچی دەتەوێ خۆم میوت؟ نا ببورە من وەکو تۆ گەمژەنیم😂🙂!**"
            return msg_text, False

        msg_text = f"**ئۆپسس😂🙂**"
        return msg_text, False

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)

    msg_text += f"**میوت کرا: {user_mention}\nلەلایەن: {admin_mention}**"

    if reason:
        msg_text += f"**هۆکار: `{reason}`\n**"
    if time:
        msg_text += f"**کات: `{time}`\n**"

    return msg_text, True


async def unmute_user(user_id, first_name, admin_id, admin_name, chat_id):
    try:
        await app.restrict_chat_member(
            chat_id,
            user_id,
            ChatPermissions(
                can_send_media_messages=True,
                can_send_messages=True,
                can_send_other_messages=True,
                can_send_polls=True,
                can_add_web_page_previews=True,
                can_invite_users=True
            )
        )
    except ChatAdminRequired:
        msg_text = "**ڕۆڵی لادانی میوتکردنم نییە، ڕۆڵی میوتم پێبدە بۆ ئەنجامدانی💘•**"
        return msg_text
    except Exception as e:
        msg_text = f"**ئۆپسس😂🙂**"
        return msg_text

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)

    msg_text = f"**میوتی لادرا: {user_mention}\nلەلایەن: {admin_mention}**"
    return msg_text


# Admin cache reload
BOT_ID = "6930664248"


@app.on_chat_member_updated()
async def admin_cache_func(_, cmu: ChatMemberUpdated):
    if cmu.old_chat_member and cmu.old_chat_member.promoted_by:
        admins_in_chat[cmu.chat.id] = {
            "last_updated_at": time(),
            "data": [
                member.user.id
                async for member in app.get_chat_members(
                    cmu.chat.id, filter="administrators"
                )
            ],
        }
        log.info(f"Updated admin cache for {cmu.chat.id} [{cmu.chat.title}]")


# Purge Messages


# Kick members


@app.on_message(filters.command(["دەرکردن", "kick"], "") & filters.group
                )
@adminsOnly("can_restrict_members")
async def kickFunc(_, message: Message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    member = await chat.get_member(admin_id)
    if member.status == enums.ChatMemberStatus.ADMINISTRATOR or member.status == enums.ChatMemberStatus.OWNER:
        if member.privileges.can_restrict_members:
            pass
        else:
            msg_text = "**تۆ ڕۆڵت نییە کەسێك دەربکەیت یان باند بکەیت🖤•**"
            return await message.reply_text(msg_text)
    else:
        msg_text = "**تۆ ڕۆڵت نییە کەسێك دەربکەیت یان باند بکەیت🖤•**"
        return await message.reply_text(msg_text)
    if not user_id:
        return await message.reply_text("**ناتوانم کەسەکە بدۆزمەوە🖤•**")
    if user_id == BOT_ID:
        return await message.reply_text(
            "**بۆچی دەتەوێ خۆم دەربکەم؟ نا ببورە من وەکو تۆ گەمژەنیم😂🙂!**"
        )
    if user_id in SUDOERS:
        return await message.reply_text("**من ناتوانم گەشەپێدەر دەربکەم بەجدیتە؟😂🙂**")
    if user_id in (await list_admins(message.chat.id)):
        return await message.reply_text(
            "**من ناتوانم ئەدمین دەربکەم بەجدیتە؟😂🙂**"
        )
    mention = (await app.get_users(user_id)).mention
    msg = f"""
**دەرکرا : {mention} **
**لەلایەن : {message.from_user.mention if message.from_user else 'Alina'} **
**هۆکار : {reason or 'No Reason Provided.'}**"""
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    await message.chat.ban_member(user_id)
    await message.reply_text(msg)
    await asyncio.sleep(1)
    await message.chat.unban_member(user_id)


# Ban members


@app.on_message(filters.command(["باند","ban", "band"], "") & filters.group)

@adminsOnly("can_restrict_members")
async def banFunc(_, message: Message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    member = await chat.get_member(admin_id)
    if member.status == enums.ChatMemberStatus.ADMINISTRATOR or member.status == enums.ChatMemberStatus.OWNER:
        if member.privileges.can_restrict_members:
            pass
        else:
            msg_text = "**تۆ ڕۆڵت نییە کەسێك دەربکەیت یان باند بکەیت🖤•**"
            return await message.reply_text(msg_text)
    else:
        msg_text = "**تۆ ڕۆڵت نییە کەسێك دەربکەیت یان باند بکەیت🖤•**"
        return await message.reply_text(msg_text)

    if not user_id:
        return await message.reply_text("**ناتوانم کەسەکە بدۆزمەوە🖤•**")
    if user_id == BOT_ID:
        return await message.reply_text(
            "**بۆچی دەتەوێ خۆم دەربکەم؟ نا ببورە من وەکو تۆ گەمژەنیم😂🙂!**"
        )
    if user_id in SUDOERS:
        return await message.reply_text(
            "**من ناتوانم گەشەپێدەر دەربکەم بەجدیتە؟😂🙂**"
        )
    if user_id in (await list_admins(message.chat.id)):
        return await message.reply_text(
            "**من ناتوانم ئەدمین دەربکەم بەجدیتە؟😂🙂**"
        )

    try:
        mention = (await app.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anony"
        )

    msg = (
        f"**باندکرا : {mention}\n**"
        f"**لەلایەن : {message.from_user.mention if message.from_user else 'Alina'}\n**"
    )
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if message.command[0] == "tban":
        split = reason.split(None, 1)
        time_value = split[0]
        temp_reason = split[1] if len(split) > 1 else ""
        temp_ban = await time_converter(message, time_value)
        msg += f"**Banned For:** {time_value}\n"
        if temp_reason:
            msg += f"**Reason:** {temp_reason}"
        try:
            if len(time_value[:-1]) < 3:
                await message.chat.ban_member(user_id, until_date=temp_ban)
                await message.reply_text(msg)
            else:
                await message.reply_text("You can't use more than 99")
        except AttributeError:
            pass
        return
    if reason:
        msg += f"**هۆکار:** {reason}"
    await message.chat.ban_member(user_id)
    await message.reply_text(msg)


# Unban members


@app.on_message(filters.command(["لادانی دەرکردن", "لادانی باند", "unban", "unband", "unkick"], "") & filters.group)
@adminsOnly("can_restrict_members")
async def unban_func(_, message: Message):
    # we don't need reasons for unban, also, we
    # don't need to get "text_mention" entity, because
    # normal users won't get text_mention if the user
    # they want to unban is not in the group.
    reply = message.reply_to_message

    if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
        return await message.reply_text("You cannot unban a channel")

    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and reply:
        user = message.reply_to_message.from_user.id
    else:
        return await message.reply_text(
            "**تکایە یوزەری بەکارهێنەر بنووسە لەگەڵ فەرمان یان وەڵامی نامەی ئەو بەکارهێنەرە بدەرەوە🖤•**"
        )
    await message.chat.unban_member(user)
    umention = (await app.get_users(user)).mention
    await message.reply_text(f"Unbanned! {umention}")


# Promote Members


@app.on_message(filters.command(["رفع مشرف", "fullpromote"], "")

                & filters.group
                )
@adminsOnly("can_promote_members")
async def promoteFunc(_, message: Message):
    user_id = await extract_user(message)
    umention = (await app.get_users(user_id)).mention
    if not user_id:
        return await message.reply_text("I can't find that user.")
    bot = await app.get_chat_member(message.chat.id, BOT_ID)
    if user_id == BOT_ID:
        return await message.reply_text("**بۆچی دەتەوێ خۆم دەربکەم؟ نا ببورە من وەکو تۆ گەمژەنیم😂🙂!**")
    if not bot.can_promote_members:
        return await message.reply_text("**ڕۆڵی دەرکردنم نییە، ڕۆڵی باندم پێبدە بۆ ئەنجامدانی💘•**")
    if message.command[0][0] == "f":
        await message.chat.promote_member(
            user_id=user_id,
            can_change_info=bot.can_change_info,
            can_invite_users=bot.can_invite_users,
            can_delete_messages=bot.can_delete_messages,
            can_restrict_members=bot.can_restrict_members,
            can_pin_messages=bot.can_pin_messages,
            can_promote_members=bot.can_promote_members,
            can_manage_chat=bot.can_manage_chat,
            can_manage_voice_chats=bot.can_manage_voice_chats,
        )
        return await message.reply_text(f"Fully Promoted! {umention}")

    await message.chat.promote_member(
        user_id=user_id,
        can_change_info=False,
        can_invite_users=bot.can_invite_users,
        can_delete_messages=bot.can_delete_messages,
        can_restrict_members=False,
        can_pin_messages=False,
        can_promote_members=False,
        can_manage_chat=bot.can_manage_chat,
        can_manage_voice_chats=bot.can_manage_voice_chats,
    )
    await message.reply_text(f"Promoted! {umention}")


# Demote Member


@app.on_message(filters.command(["تنزيل مشرف"], "") & filters.group)
@adminsOnly("can_promote_members")
async def demote(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("I can't find that user.")
    if user_id == BOT_ID:
        return await message.reply_text("I can't demote myself.")
    if user_id in SUDOERS:
        return await message.reply_text(
            "You wanna demote the elevated one?, RECONSIDER!"
        )
    await message.chat.promote_member(
        user_id=user_id,
        can_change_info=False,
        can_invite_users=False,
        can_delete_messages=False,
        can_restrict_members=False,
        can_pin_messages=False,
        can_promote_members=False,
        can_manage_chat=False,
        can_manage_voice_chats=False,
    )
    umention = (await app.get_users(user_id)).mention
    await message.reply_text(f"Demoted! {umention}")


# Pin Messages


# Mute members


@app.on_message(filters.command(["ئاگاداری", "میوت", "mute"], "") & filters.group
                )
@adminsOnly("can_restrict_members")
async def mute(_, message: Message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    member = await chat.get_member(admin_id)
    if member.status == enums.ChatMemberStatus.ADMINISTRATOR or member.status == enums.ChatMemberStatus.OWNER:
        if member.privileges.can_restrict_members:
            pass
        else:
            msg_text = "**تۆ ڕۆڵت نییە کەسێك میوت بکەیت🖤•****"
            return await message.reply_text(msg_text)
    else:
        msg_text = "**تۆ ڕۆڵت نییە کەسێك میوت بکەیت🖤•**"
        return await message.reply_text(msg_text)
    if not user_id:
        return await message.reply_text("**ناتوانم کەسەکە بدۆزمەوە🖤•**")
    if user_id == BOT_ID:
        return await message.reply_text("**بۆچی دەتەوێ خۆم دەربکەم؟ نا ببورە من وەکو تۆ گەمژەنیم😂🙂!**")
    if user_id in SUDOERS:
        return await message.reply_text(
            "**من ناتوانم گەشەپێدەر دەربکەم بەجدیتە؟😂🙂**"
        )
    if user_id in (await list_admins(message.chat.id)):
        return await message.reply_text(
            "**من ناتوانم ئەدمین دەربکەم بەجدیتە؟😂🙂**"
        )
    mention = (await app.get_users(user_id)).mention
    keyboard = ikb({"🚨 لادانی ئاگاداری 🚨": f"unmute_{user_id}"})
    msg = (
        f"**میوت کرا : {mention}\n**"
        f"**لەلایەن : {message.from_user.mention if message.from_user else 'Alina'}\n**"
    )
    photo = (f"https://telegra.ph/file/f0f3e316bebd894baa110.jpg")
    if message.command[0] == "tmute":
        split = reason.split(None, 1)
        time_value = split[0]
        temp_reason = split[1] if len(split) > 1 else ""
        temp_mute = await time_converter(message, time_value)
        msg += f"**Muted For:** {time_value}\n"
        if temp_reason:
            msg += f"**Reason:** {temp_reason}"
        try:
            if len(time_value[:-1]) < 3:
                await message.chat.restrict_member(
                    user_id,
                    permissions=ChatPermissions(),
                    until_date=temp_mute,
                )
                await message.reply_photo(photo, caption=msg, reply_markup=keyboard)
            else:
                await message.reply_text("You can't use more than 99")
        except AttributeError:
            pass
        return
    if reason:
        msg += f"**Reason:** {reason}"
    await message.chat.restrict_member(user_id, permissions=ChatPermissions())
    await message.reply_photo(photo, caption=msg, reply_markup=keyboard)


# Unmute members


@app.on_message(filters.command(["لادانی ئاگاداری", "unmute", "unmute_", "لادانی میوت"], "") & filters.group)
@adminsOnly("can_restrict_members")
async def unmute(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("**ناتوانم کەسەکە بدۆزمەوە🖤•**")
    await message.chat.unban_member(user_id)
    umention = (await app.get_users(user_id)).mention
    await message.reply_text(f"**میوتی لادرا {umention}**")


# Ban deleted accounts


@app.on_message(filters.command("حظر خفي")
                & filters.group

                )
@adminsOnly("can_restrict_members")
async def ban_deleted_accounts(_, message: Message):
    chat_id = message.chat.id
    deleted_users = []
    banned_users = 0
    m = await message.reply("Finding ghosts...")

    async for i in app.get_chat_members(chat_id):
        if i.user.is_deleted:
            deleted_users.append(i.user.id)
    if len(deleted_users) > 0:
        for deleted_user in deleted_users:
            try:
                await message.chat.ban_member(deleted_user)
            except Exception:
                pass
            banned_users += 1
        await m.edit(f"Banned {banned_users} Deleted Accounts")
    else:
        await m.edit("There are no deleted accounts in this chat")


@app.on_message(filters.command(["warn", "dwarn", "تحذير", "انذار"], "") & filters.group
                )
@adminsOnly("can_restrict_members")
async def warn_user(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    chat_id = message.chat.id
    if not user_id:
        return await message.reply_text("I can't find that user.")
    if user_id == BOT_ID:
        return await message.reply_text(
            "I can't warn myself, i can leave if you want."
        )
    if user_id in SUDOERS:
        return await message.reply_text(
            "You Wanna Warn The Elevated One?, RECONSIDER!"
        )
    if user_id in (await list_admins(chat_id)):
        return await message.reply_text(
            "I can't warn an admin, You know the rules, so do i."
        )
    user, warns = await asyncio.gather(
        app.get_users(user_id),
        get_warn(chat_id, await int_to_alpha(user_id)),
    )
    mention = user.mention
    keyboard = ikb({"🚨  حذف التحذير  🚨": f"unwarn_{user_id}"})
    if warns:
        warns = warns["warns"]
    else:
        warns = 0
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if warns >= 2:
        await message.chat.ban_member(user_id)
        await message.reply_text(
            f"Number of warns of {mention} exceeded, BANNED!"
        )
        await remove_warns(chat_id, await int_to_alpha(user_id))
    else:
        warn = {"warns": warns + 1}
        msg = f"""
**حذرت :** {mention}
**يا:** {message.from_user.mention if message.from_user else 'Alina'}
**السبب:** {reason or 'No Reason Provided.'}
**التحذيرات المتبقيه:** {warns + 1}/3"""
        await message.reply_text(msg, reply_markup=keyboard)
        await add_warn(chat_id, await int_to_alpha(user_id), warn)


@app.on_callback_query(filters.regex("unwarn_"))
async def remove_warning(_, cq: CallbackQuery):
    from_user = cq.from_user
    chat_id = cq.message.chat.id
    permissions = await member_permissions(chat_id, from_user.id)
    permission = "can_restrict_members"
    if permission not in permissions:
        return await cq.answer(
            "You don't have enough permissions to perform this action.\n"
            + f"Permission needed: {permission}",
            show_alert=True,
        )
    user_id = cq.data.split("_")[1]
    warns = await get_warn(chat_id, await int_to_alpha(user_id))
    if warns:
        warns = warns["warns"]
    if not warns or warns == 0:
        return await cq.answer("User has no warnings.")
    warn = {"warns": warns - 1}
    await add_warn(chat_id, await int_to_alpha(user_id), warn)
    text = cq.message.text.markdown
    text = f"~~{text}~~\n\n"
    text += f"__Warn removed by {from_user.mention}__"
    await cq.message.edit(text)


# Rmwarns


@app.on_message(filters.command(["حذف التحذير", "حذف الاندارات"], "") & filters.group
                )
@adminsOnly("can_restrict_members")
async def remove_warnings(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a message to remove a user's warnings."
        )
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    chat_id = message.chat.id
    warns = await get_warn(chat_id, await int_to_alpha(user_id))
    if warns:
        warns = warns["warns"]
    if warns == 0 or not warns:
        await message.reply_text(f"{mention} have no warnings.")
    else:
        await remove_warns(chat_id, await int_to_alpha(user_id))
        await message.reply_text(f"Removed warnings of {mention}.")


# Warns


@app.on_message(filters.command(["التحذيرات", "الانذارات"], "") & filters.group)
@capture_err
async def check_warns(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("I can't find that user.")
    warns = await get_warn(message.chat.id, await int_to_alpha(user_id))
    mention = (await app.get_users(user_id)).mention
    if warns:
        warns = warns["warns"]
    else:
        return await message.reply_text(f"{mention} has no warnings.")
    return await message.reply_text(f"{mention} has {warns}/3 warnings.")


# Report


@app.on_message(
    (filters.command("ابلاغ")
     | filters.command(["admins", "admin"], prefixes="@")
     )

    & filters.group
)
@capture_err
async def report_user(_, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a message to report that user."
        )

    reply = message.reply_to_message
    reply_id = reply.from_user.id if reply.from_user else reply.sender_chat.id
    user_id = message.from_user.id if message.from_user else message.sender_chat.id
    if reply_id == user_id:
        return await message.reply_text("Why are you reporting yourself ?")

    list_of_admins = await list_admins(message.chat.id)
    linked_chat = (await app.get_chat(message.chat.id)).linked_chat
    if linked_chat is not None:
        if reply_id in list_of_admins or reply_id == message.chat.id or reply_id == linked_chat.id:
            return await message.reply_text(
                "Do you know that the user you are replying is an admin ?"
            )
    else:
        if reply_id in list_of_admins or reply_id == message.chat.id:
            return await message.reply_text(
                "Do you know that the user you are replying is an admin ?"
            )

    user_mention = reply.from_user.mention if reply.from_user else reply.sender_chat.title
    text = f"Reported {user_mention} to admins!"
    admin_data = await app.get_chat_members(
        chat_id=message.chat.id, filter="administrators"
    )  # will it giv floods ?
    for admin in admin_data:
        if admin.user.is_bot or admin.user.is_deleted:
            # return bots or deleted admins
            continue
        text += f"[\u2063](tg://user?id={admin.user.id})"

    await message.reply_to_message.reply_text(text)
