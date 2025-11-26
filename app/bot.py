from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from app.config.config import config
from app.config.logging import get_logger
from app.db.session import db
from app.dialogs import dialogs
from app.handlers import routers
from app.middlewares import setup_middlewares

logger = get_logger("bot")


class TelegramBot:
    def __init__(self):
        self.bot = None
        self.dp = None
        self.registry = None
        self._is_initialized = False

    async def initialize(self):
        if self._is_initialized:
            logger.warning("Bot is already initialized")
            return

        logger.info("Initializing Telegram bot...")

        try:
            await db.init()

            self.bot = Bot(
                token=config.BOT_TOKEN,
                default=DefaultBotProperties(
                    parse_mode=ParseMode.HTML, link_preview_is_disabled=True
                ),
            )

            storage = MemoryStorage()
            self.dp = Dispatcher(storage=storage)

            self.dp["config"] = config

            self.setup_middlewares_and_routers()

            self._is_initialized = True
            logger.info("Telegram bot initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize bot: {e}")
            raise

    def setup_middlewares_and_routers(self):
        setup_middlewares(self.dp)

        for router in routers:
            self.dp.include_router(router)

        for dialog in dialogs:
            self.dp.include_router(dialog)

        setup_dialogs(self.dp)

    async def start_polling(self):
        if not self._is_initialized:
            await self.initialize()

        logger.info("Starting bot polling...")
        try:
            await self.dp.start_polling(self.bot)
        except Exception as e:
            logger.error(f"Polling error: {e}")
            raise

    async def stop(self):
        logger.info("Stopping bot...")

        if hasattr(self, "dp") and self.dp:
            await self.dp.storage.close()

        await db.close()
        self._is_initialized = False
        logger.info("Bot stopped successfully")


telegram_bot = TelegramBot()
