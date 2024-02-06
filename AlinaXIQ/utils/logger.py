from pyrogram.enums import ParseMode

from AlinaXIQ import app
from AlinaXIQ.utils.database import is_on_off
from config import LOGGER_ID


async def play_logs(message, streamtype):
    if await is_on_off(2):
        logger_text = f"""
<b>{app.mention} پەخشی گرووپەکان</b>

<b>ئایدی گرووپ :</b> <code>{message.chat.id}</code>
<b>ناوی گرووپ :</b> {message.chat.title}
<b>یوزەری گرووپ :</b> @{message.chat.username}

<b>ئایدی بەکارهێنەر :</b> <code>{message.from_user.id}</code>
<b>ناو :</b> {message.from_user.mention}
<b>یوزەر :</b> @{message.from_user.username}

<b>ناوی گۆرانی :</b> {message.text.split(None, 1)[1]}
<b>جۆری پلاتفۆڕم :</b> {streamtype}"""
        if message.chat.id != LOGGER_ID:
            try:
                await app.send_message(
                    chat_id=LOGGER_ID,
                    text=logger_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except:
                pass
        return
