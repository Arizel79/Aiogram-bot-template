from app.dialogs.settings.shared import *
from app.keyboards import get_main_keyboard


async def on_language_selected(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    new_language_key = button.widget_id
    user = dialog_manager.middleware_data.get("user")
    user_service: UserService = dialog_manager.middleware_data.get("user_service")
    i18n = dialog_manager.middleware_data.get("i18n")
    bot = dialog_manager.middleware_data.get("bot")

    if user and user_service and i18n and bot:
        await user_service.update_user_language(user, new_language_key)
        i18n.locale = new_language_key

        new_keyboard = get_main_keyboard(i18n)

        await callback.message.delete()
        await dialog_manager.done()

        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=i18n.get(
                "settings-language-changed", language=new_language_key.upper()
            ),
            reply_markup=new_keyboard,
        )

    else:
        await dialog_manager.back()


async def get_language_data(dialog_manager: DialogManager, **kwargs):
    user = dialog_manager.middleware_data.get("user")
    i18n = dialog_manager.middleware_data.get("i18n")

    data = {
        "current_language": user.language.upper() if user else "RU",
    }

    if i18n:
        data.update(
            {
                "choose_language": i18n.get("settings-choose-language"),
                "current_language_label": i18n.get(
                    "settings-current-language", language=data["current_language"]
                ),
            }
        )

    return data


language_window = Window(
    Format("{choose_language}"),
    Format("\n{current_language_label}"),
    Row(
        Button(
            I18NFormat("ru-language-button"), id="ru", on_click=on_language_selected
        ),
        Button(
            I18NFormat("en-language-button"), id="en", on_click=on_language_selected
        ),
    ),
    Back(I18NFormat("back-button")),
    state=SettingsStates.language,
    getter=get_language_data,
)
