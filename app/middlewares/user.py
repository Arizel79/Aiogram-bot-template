from aiogram import BaseMiddleware
from aiogram.types import Update, User as TgUser
from typing import Any, Dict, Callable, Awaitable

from app.services.user_service import UserService


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        telegram_user: TgUser = data.get("event_from_user")
        user_service: UserService = data.get("user_service")

        if telegram_user and user_service:
            user = await user_service.get_or_create_user(
                telegram_id=telegram_user.id,
                username=telegram_user.username,
                first_name=telegram_user.first_name,
                last_name=telegram_user.last_name,
            )
            data["user"] = user

        return await handler(event, data)
