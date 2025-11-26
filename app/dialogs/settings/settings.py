from app.dialogs.settings.shared import *


async def get_settings_data(dialog_manager: DialogManager, **kwargs):
    user = dialog_manager.middleware_data.get("user")
    i18n = dialog_manager.middleware_data.get("i18n")

    data = {
        "name": user.first_name if user else "User",
        "current_language": user.language.upper() if user else "RU",
    }

    if i18n:
        data.update(
            {
                "settings_title": i18n.get("settings-title"),
                "current_language_label": i18n.get(
                    "settings-current-language", language=data["current_language"]
                ),
            }
        )

    return data


async def go_to_language_settings(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    await dialog_manager.switch_to(SettingsStates.language)


settings_main_window = Window(
    Format("{settings_title}"),
    Format("\n{current_language_label}"),
    Row(
        Button(
            I18NFormat("settings-change-language-button"),
            id="change_language",
            on_click=go_to_language_settings,
        ),
    ),
    state=SettingsStates.main,
    getter=get_settings_data,
)
