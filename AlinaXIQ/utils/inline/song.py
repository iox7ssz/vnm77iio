from pyrogram.types import InlineKeyboardButton
import config 

def song_markup(_, vidid):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"song_helper audio|{vidid}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"song_helper video|{vidid}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_6"], url=config.SUPPORT_CHANNEL
            ),
        ],
    ]
    return buttons
