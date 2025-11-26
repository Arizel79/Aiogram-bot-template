from typing import Any, Dict, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_i18n import I18nContext
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore

from app.config import get_handler_logger

logger = get_handler_logger("current_locale")
from app.config import config

i18n_middleware = I18nMiddleware(
    core=FluentRuntimeCore(
        path=config.locales.locales_dir,
        default_locale=config.locales.default_locale,
    )
)


class CurrentLocaleMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, event, data: Dict[str, Any]) -> Any:
        user = data.get("user")
        i18n: I18nContext = data.get("i18n")

        if user and i18n and hasattr(user, "language") and user.language:
            i18n.locale = user.language

        return await handler(event, data)
