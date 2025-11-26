from aiogram import Router

from app.handlers.common.start import router as start_router
from app.handlers.common.help import router as help_router
from app.handlers.common.settings import router as settings_router

router = Router()

router.include_router(start_router)
router.include_router(help_router)
router.include_router(settings_router)

__all__ = ("router",)
