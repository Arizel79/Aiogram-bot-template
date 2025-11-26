from typing import Union
from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram_i18n import I18nContext


class I18nKeyFilter(BaseFilter):
    def __init__(self, key: str):
        self.key = key

    async def __call__(self, message: Message, i18n: I18nContext) -> bool:
        if not message.text:
            return False

        expected_text = i18n.get(self.key)
        return message.text == expected_text
