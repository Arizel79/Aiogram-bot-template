from typing import Any, Dict, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Update
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import config, get_logger
from app.services.user_service import UserService

logger = get_logger("middleware.service")


class ServiceMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        session: AsyncSession = data.get("session")

        if session:
            data["config"] = config
            data["user_service"] = UserService(session)

        return await handler(event, data)
