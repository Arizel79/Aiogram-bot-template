from typing import Union
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class PrivateChatFilter(BaseFilter):
    async def __call__(self, update: Union[Message, CallbackQuery]) -> bool:
        if isinstance(update, Message):
            chat_type = update.chat.type
        elif isinstance(update, CallbackQuery) and update.message:
            chat_type = update.message.chat.type
        else:
            return False

        return chat_type == "private"