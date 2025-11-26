import json
from pathlib import Path

from app.config.logging import get_logger

logger = get_logger("config")


class ConfigClass:
    def load_config(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            logger.info(f"Config loaded: {self.config_path}")
            dict_ = json.load(f)
            self.config = dict_

    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = {}
        self.load_config()

        self.BASE_DIR = Path(__file__).parent.parent

        self.DATABASE_CONFIG = self.config.get("database")
        self.DATABASE_URL = self.DATABASE_CONFIG["db"]

        self.FSM = self.config.get("fsm", {})
        self.FSM_TYPE = self.FSM.get("type", "default")
        if self.FSM_TYPE == "redis":
            self.FSM_REDIS_URL = self.FSM.get("redis_url")

        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL is required!")

        self.BOT_TOKEN = self.config.get("bot").get("token")

        if not self.BOT_TOKEN or ":" not in self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN required!")

        self.LOCALES_CONFIG = self.config.get("locales", {})
        self.AVAILABLE_LOCALES = self.LOCALES_CONFIG.get("locales", "en")
        self.DEFAULT_LOCALE = self.LOCALES_CONFIG.get("default_locale", "en")
        assert self.DEFAULT_LOCALE in self.AVAILABLE_LOCALES

        self.LOCALES_DIR = str(self.BASE_DIR.parent / "locales")


config = ConfigClass()
