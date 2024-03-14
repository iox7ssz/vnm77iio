from pyrogram import filters
from pyrogram.types import Message

from AlinaXIQ import app
from AlinaXIQ.utils.database import get_loop, set_loop
from AlinaXIQ.utils.decorators import AdminRightsCheck
from AlinaXIQ.utils.inline import close_markup
from config import BANNED_USERS


@app.on_message(filters.command(["/loop", "/cloop", "دووبارەکردنەوە"], "") & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def admins(cli, message: Message, _, chat_id):
    usage = _["admin_17"]
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip()
    user_mention = message.from_user.mention if message.from_user else "𝖠𝖽𝗆𝗂𝗇"
    if state.isnumeric():
        state = int(state)
        if 1 <= state <= 10:
            got = await get_loop(chat_id)
            if got != 0:
                state = got + state
            if int(state) > 10:
                state = 10
            await set_loop(chat_id, state)
            return await message.reply_text(
                text=_["admin_18"].format(state, user_mention),
                reply_markup=close_markup(_),
            )
        else:
            return await message.reply_text(_["admin_17"])
    elif state.lower() == "enable" or state.lower() == "چالاک":
        await set_loop(chat_id, 10)
        return await message.reply_text(
            text=_["admin_18"].format(state, user_mention),
            reply_markup=close_markup(_),
        )
    elif state.lower() == "disable" or state.lower() == "ناچالاک":
        await set_loop(chat_id, 0)
        return await message.reply_text(
            _["admin_19"].format(user_mention),
            reply_markup=close_markup(_),
        )
    else:
        return await message.reply_text(usage)
