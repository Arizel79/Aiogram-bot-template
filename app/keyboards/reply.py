from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram_i18n import I18nContext


def get_main_keyboard(i18n: I18nContext) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=i18n.get("settings-button")),
                KeyboardButton(text=i18n.get("random-number-button")),
            ]
        ],
        resize_keyboard=True,
        persistent=True,
    )