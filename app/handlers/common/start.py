from decimal import Decimal
from aiogram import Router, types
from aiogram.filters import Command
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.services.user_service import UserService
from app.keyboards import get_main_keyboard  # Добавляем импорт

router = Router()


@router.message(Command("start"))
async def start_handler(
    message: types.Message,
    user: User,
    session: AsyncSession,
    user_service: UserService,
    i18n: I18nContext,
):
    reply_markup = get_main_keyboard(i18n)

    await message.answer(
        i18n.get("start-message", name=user.first_name), reply_markup=reply_markup
    )
