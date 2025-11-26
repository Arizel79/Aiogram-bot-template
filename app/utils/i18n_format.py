from typing import Any
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text
from aiogram_i18n import I18nContext

I18N_FORMAT_KEY = "aiogd_i18n_format"


class I18NFormat(Text):
    def __init__(self, text: str, when: WhenCondition = None):
        super().__init__(when)
        self.text = text

    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        i18n: I18nContext = manager.middleware_data.get("i18n")
        if i18n:
            translated = i18n.get(self.text)
            if data:
                return translated.format(**data)

            return translated

        return self.text
