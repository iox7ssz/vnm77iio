from pyrogram import filters
from pyrogram.types import Message
from strings.filters import command
from AlinaXIQ import app
from AlinaXIQ.core.call import Alina
from AlinaXIQ.utils.database import is_music_playing, music_off
from AlinaXIQ.utils.decorators import AdminRightsCheck
from AlinaXIQ.utils.inline import close_markup
from config import BANNED_USERS


@app.on_message(command(["pause", "cpause","/pause","/cpause","وسبە","وەستانی کاتی"]) & ~filters.private & ~BANNED_USERS)
@AdminRightsCheck
async def pause_admin(cli, message: Message, _, chat_id):
    if not await is_music_playing(chat_id):
        return await message.reply_text(_["admin_1"])
    await music_off(chat_id)
    user_mention = message.from_user.mention if message.from_user else "𝖠𝖽𝗆𝗂𝗇"
    await Alina.pause_stream(chat_id)
    await message.reply_text(
        _["admin_2"].format(message.from_user.mention), reply_markup=close_markup(_)
    )
