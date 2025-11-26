from aiogram import Router, types
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode

from app.config import get_handler_logger
from app.dialogs.settings import SettingsStates
from app.filters import I18nKeyFilter

logger = get_handler_logger("reply_keyboard")

router = Router()


@router.message(I18nKeyFilter("settings-button"))
@router.message(Command("settings"))
async def settings_handler(message: types.Message, dialog_manager: DialogManager):
    logger.info("view settings")
    await dialog_manager.start(SettingsStates.main, mode=StartMode.RESET_STACK)
