from aiogram import Router, types
from aiogram.filters import Command
from aiogram_i18n import I18nContext

from app.db.models import User

router = Router()


@router.message(Command("help"))
async def help_handler(
    message: types.Message,
    i18n: I18nContext,
    user: User,
):
    await message.answer(i18n.get("help-message"))
