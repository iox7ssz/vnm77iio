import requests
from bs4 import BeautifulSoup as  BSP
from AlinaXIQ import app as Alina
from pyrogram import filters
url = "https://all-hashtag.com/library/contents/ajax_generator.php"

@Alina.on_message(filters.command("hashtag"))
async def hastag(bot, message):
    global content
    try:
        text = message.text.split(' ',1)[1]
        data = dict(keyword=text, filter="top")

        res = requests.post(url, data).text

        content = BSP(res, 'html.parser').find("div", {"class":"copy-hashtags"}).string
    except IndexError:
        return await message.reply_text("**نموونە :\n\n/hashtag Kuridstan**")
        
    
    await message.reply_text(f"ʜᴇʀᴇ ɪs ʏᴏᴜʀ  ʜᴀsᴛᴀɢ :\n<pre>{content}</pre>", quote=True)
    
mod_name = "Hᴀsʜᴛᴀɢ"
help= """
Yᴏᴜ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ʜᴀsʜᴛᴀɢ ɢᴇɴᴇʀᴀᴛᴏʀ ᴡʜɪᴄʜ ᴡɪʟʟ ɢɪᴠᴇ ʏᴏᴜ ᴛʜᴇ ᴛᴏᴘ 𝟹𝟶 ᴀɴᴅ ᴍᴏʀᴇ ʜᴀsʜᴛᴀɢs ʙᴀsᴇᴅ ᴏғғ ᴏғ ᴏɴᴇ ᴋᴇʏᴡᴏʀᴅ sᴇʟᴇᴄᴛɪᴏɴ.
° /hastag enter word to generate hastag.
°Exᴀᴍᴘʟᴇ:  /hastag python """
