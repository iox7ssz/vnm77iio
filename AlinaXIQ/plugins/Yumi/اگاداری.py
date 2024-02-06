from pyrogram import Client, filters
from strings.filters import command
from AlinaXIQ import app
from AlinaXIQ.utils.Alina_ban import admin_filter

7amo = {}
Alina_IQ = 3

@app.on_message(command("ئاگاداربە") & admin_filter)
async def alinaa(client, message):
    me = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    if chat_id not in 7amo:
        7amo[chat_id] = {}
    if user_id not in 7amo[chat_id]:
        7amo[chat_id][user_id] = 1
    else:
        7amo[chat_id][user_id] += 1
    await message.reply_text(f"{7amo[chat_id][user_id]}")
    if 7amo[chat_id][user_id] >= Alina_IQ:
        try:
        	del 7amo[chat_id][user_id]
        	await client.ban_chat_member(chat_id, user_id)
        	await message.reply("**دەرکرا♥️✅•**")   	
        except:
        	await message.reply("**نەدۆزرایەوە**")
        
