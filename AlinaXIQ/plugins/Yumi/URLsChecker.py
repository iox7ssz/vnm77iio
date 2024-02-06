from pyrogram import Client, filters
from pyrogram.types import Message
from DAXXMUSIC import app
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import pyrogram.errors, requests, re



@app.on_message(filters.command(["chk","پشکنین","پشکنين"], prefixes=["/", "", "#"]))
async def huhh(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/024f02f6681c3785ec085.jpg",
        caption=f"""**[⧉• 𝙎𝙊𝙐𝙍𝘾𝞝 𝙄𝙌 - فەرمانی پشکنین🧑🏻‍💻🖤](t.me/MGIMT)**\n\n**بەخێربێی ئەزیزم {message.from_user.mention} بۆ بەشی پشکنینی لینك تایبەت بە سەرچاوەی زیرەك**\n** بۆ بەکارهێنانی: بڕۆ چاتی بۆت @IQMCBOT و لینك دابنێ بۆتی دەپشکنێ پێت دەڵێت پارێزراوە یان نا♥⚡**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                                        InlineKeyboardButton(
                        "𝙄𝙌 𝙈𝙐𝙎𝙄𝘾 ♥️•", url=f"https://t.me/IQMCBOT"), 
                 ],[
                
                    InlineKeyboardButton(
                        "⧉• 𝙎𝙊𝙐𝙍𝘾𝞝 𝙄𝙌", url=f"https://t.me/MGIMT"),
                ],

            ]

        ),

    )

    
