from aiogram import Dispatcher

from app.middlewares.database import DatabaseMiddleware
from app.middlewares.i18n import i18n_middleware, CurrentLocaleMiddleware
from app.middlewares.logging import LoggingMiddleware
from app.middlewares.service import ServiceMiddleware
from app.middlewares.user import UserMiddleware
from app.middlewares.throttling import ThrottlingMiddleware


def setup_middlewares(dp: Dispatcher):
    i18n_middleware.setup(dp)

    dp.update.outer_middleware(LoggingMiddleware())
    dp.update.outer_middleware(DatabaseMiddleware())
    dp.update.outer_middleware(ServiceMiddleware())
    dp.update.outer_middleware(UserMiddleware())
    dp.update.outer_middleware(CurrentLocaleMiddleware())

    dp.update.outer_middleware(ThrottlingMiddleware(5, 2))
