from aiogram import Router, types
from aiogram_i18n import I18nContext

from app.handlers.common.unknown_message import router as unknown_message_router

from app.handlers.common.start import router as start_router
from app.handlers.common.help import router as help_router
from app.handlers.common.settings import router as settings_router
from app.handlers.common.random_number import router as random_number_router

router = Router()

router.include_router(start_router)
router.include_router(help_router)
router.include_router(settings_router)
router.include_router(random_number_router)
router.include_router(unknown_message_router)


__all__ = ("router",)