from aiogram import Router, types
from aiogram.filters import Command
from aiogram_i18n import I18nContext

from app.db.models import User

router = Router()


@router.message(Command("ping"))
async def ping_handler(
    message: types.Message,
    i18n: I18nContext,
    user: User,
):
    await message.reply(i18n.get("pong-message"))
