from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Row, Back
from aiogram_dialog.widgets.text import Format

from app.services.user_service import UserService
from app.utils.i18n_format import I18NFormat


class SettingsStates(StatesGroup):
    main = State()
    language = State()
    random_number = State()
