from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import SUPPORT_CHANNEL


def botplaylist_markup(_):
    buttons = [
        [
            InlineKeyboardButton(text=_["S_B_6"], url=SUPPORT_CHANNEL),
        ],[
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
        ],
    ]
    return buttons


def close_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ]
        ]
    )
    return upl


def supp_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["S_B_6"],
                    url=SUPPORT_CHANNEL,
                ),
            ]
        ]
    )
    return upl
