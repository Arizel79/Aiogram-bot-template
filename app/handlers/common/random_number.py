from aiogram import Router, types
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode

from app.config import get_handler_logger
from app.dialogs.random_number.random_number import RandomNumberStates
from app.filters import I18nKeyFilter

logger = get_handler_logger("random_number")

router = Router()


@router.message(I18nKeyFilter("random-number-button"))
@router.message(Command("random"))
async def random_number_handler(
        message: types.Message,
        dialog_manager: DialogManager
):
    logger.info("start random number dialog")
    await dialog_manager.start(RandomNumberStates.main, mode=StartMode.RESET_STACK)