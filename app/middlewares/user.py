from typing import Any, Dict, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Update, User as TgUser

from app.config import config, get_middleware_logger
from app.services.user_service import UserService

logger = get_middleware_logger("user")


class UserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any],
    ) -> Any:
        telegram_user: TgUser = data.get("event_from_user")
        user_service: UserService = data.get("user_service")

        telegram_user_language = None
        if not telegram_user.language_code is None:
            telegram_user_language = telegram_user.language_code.split('-')[0]


        if telegram_user_language in config.locales.available_locales:
            language = telegram_user.language_code
        else:
            language = config.locales.default_locale

        if telegram_user and user_service:
            user = await user_service.get_or_create_user(
                telegram_id=telegram_user.id,
                username=telegram_user.username,
                first_name=telegram_user.first_name,
                last_name=telegram_user.last_name,
                language=language
            )
            data["user"] = user

        return await handler(event, data)
