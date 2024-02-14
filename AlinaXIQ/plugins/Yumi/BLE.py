import asyncio
import random
from pyrogram import Client, filters, idle
from AlinaXIQ import app
from strings.filters import command


SLEEP = 0.1


@app.on_message(filters.regex("^بڵێ|^بلی") & filters.group)
async def say(app, message):
    if message.text.startswith("بلی") and message.reply_to_message:
        txt = message.text.split(None, 1)[1]
        return await message.reply_to_message.reply(txt)

    elif message.text.startswith("بڵێ"):
        txt = message.text.split(None, 1)[1]
        return await message.reply(txt)


@app.on_message(command(["heart", "دڵ","دڵم","dlm","دل"]))
async def hearts(app, message):
    await asyncio.sleep(SLEEP * 3)
    await message.edit("**❤️ 𝖨**")
    await asyncio.sleep(0.5)
    await message.edit("**❤️ 𝖨 𝖫𝗈𝗏𝖾**")
    await asyncio.sleep(0.5)
    await message.edit("**❤️ 𝖨 𝖫𝗈𝗏𝖾 𝖸𝗈𝗎**")
    await asyncio.sleep(3)
    await message.edit("**❤️ 𝖨 𝖫𝗈𝗏𝖾 𝖸𝗈𝗎 <3**")
