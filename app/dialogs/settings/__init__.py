from aiogram_dialog import Dialog, LaunchMode
from app.dialogs.settings.shared import *

from app.dialogs.settings.language import language_window
from app.dialogs.settings.settings import settings_main_window

settings_dialog = Dialog(
    settings_main_window, language_window, launch_mode=LaunchMode.EXCLUSIVE
)
