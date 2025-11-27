import random

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, StartMode, LaunchMode
from aiogram_dialog.widgets.kbd import Button, Row, Cancel
from aiogram_dialog.widgets.text import Format

from app.utils.i18n_format import I18NFormat


class RandomNumberStates(StatesGroup):
    main = State()


def get_random_number():
    return random.randint(0, 100)


async def get_random_number_data(dialog_manager: DialogManager, **kwargs):
    current_number = dialog_manager.dialog_data.get("random_number", get_random_number())
    i18n = dialog_manager.middleware_data.get("i18n")

    data = {
        "current_number": current_number,
    }

    if i18n:
        data.update({
            "random_number_title": i18n.get("random-number-title"),
            "current_number_label": i18n.get("random-current-number", number=current_number),
        })

    return data


async def generate_random_number(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    new_number = get_random_number()
    dialog_manager.dialog_data["random_number"] = new_number
    await dialog_manager.show()


async def on_dialog_close(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    await dialog_manager.done()


random_number_dialog = Dialog(
    Window(
        Format("{random_number_title}"),
        Format("\n{current_number_label}"),
        Row(
            Button(
                I18NFormat("generate-number-button"),
                id="generate_random_number",
                on_click=generate_random_number
            ),
        ),
        Cancel(
            I18NFormat("back-button"),
        ),
        state=RandomNumberStates.main,
        getter=get_random_number_data,

    ),
launch_mode=LaunchMode.SINGLE_TOP
)