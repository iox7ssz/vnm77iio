import pyrogram
from pyrogram import filters, Client
from pyrogram.enums import ChatMemberStatus
from AlinaXIQ import app


@app.on_message(filters.forwarded)
def gjgh(client, m):
    global id
    su = client.get_chat_member(m.chat.id, m.from_user.id).status
    if str(su) == "ChatMemberStatus.MEMBER":
        m.delete()
