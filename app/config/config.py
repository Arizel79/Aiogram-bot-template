import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional, List
from app.config.logging import get_logger

logger = get_logger("config")


class DatabaseConfig:
    def __init__(self, config: Dict[str, Any]):
        self.url = config.get("db")
        self.echo = config.get("echo", False)
        self.pool_size = config.get("pool_size", 20)
        self.max_overflow = config.get("max_overflow", 30)
        self._validate()

    def _validate(self):
        if not self.url:
            raise ValueError("DATABASE_URL is required!")


class BotConfig:
    def __init__(self, config: Dict[str, Any]):
        self.token = os.getenv("BOT_TOKEN") or config.get("token")
        self.admins: List[int] = config.get("admins", [])
        self.webhook_url = config.get("webhook_url")
        self.webhook_path = config.get("webhook_path")
        self.use_webhook = config.get("use_webhook", False)
        self._validate()

    def _validate(self):
        if not self.token:
            raise ValueError("BOT_TOKEN is required!")
        if ":" not in self.token:
            raise ValueError("Invalid BOT_TOKEN format!")

    @property
    def is_webhook_mode(self) -> bool:
        return self.use_webhook and bool(self.webhook_url)


class FSMConfig:
    def __init__(self, config: Dict[str, Any]):
        self.type = config.get("type", "memory")
        self.redis_url = config.get("redis_url")

    @property
    def is_redis(self) -> bool:
        return self.type == "redis"


class LocalesConfig:
    def __init__(self, config: Dict[str, Any], base_dir: Path):
        self.default_locale = config.get("default_locale", "en")
        self.available_locales = config.get("locales", ["en", "ru"])
        self.locales_dir = str(base_dir.parent / "locales")
        self._validate()

    def _validate(self):
        if self.default_locale not in self.available_locales:
            raise ValueError(f"DEFAULT_LOCALE '{self.default_locale}' not in AVAILABLE_LOCALES")

    def is_locale_available(self, locale: str) -> bool:
        return locale in self.available_locales


class LoggingConfig:
    def __init__(self, config: Dict[str, Any]):
        self.level = config.get("level", "INFO")
        self.write_to_files = config.get("write_to_files", True)
        self.rotation = config.get("rotation", "10 MB")
        self.retention = config.get("retention", "30 days")


class RedisConfig:
    def __init__(self, config: Dict[str, Any]):
        self.url = config.get("url", "redis://localhost:6379/0")
        self.use_redis = config.get("use_redis", False)


class Config:
    def __init__(self, config_path: Optional[str] = None):
        self.BASE_DIR = Path(__file__).parent.parent

        if config_path:
            self.config_path = Path(config_path)
        else:
            self.config_path = self.BASE_DIR.parent / "config.yaml"

        if not self.config_path.exists():
            raise FileNotFoundError(f'Config file "{self.config_path}" not found')

        if self.config_path.suffix.lower() not in ['.yaml', '.yml']:
            raise ValueError(f'Config file must be YAML (.yaml or .yml), got: {self.config_path.suffix}')

        self.config = self.load_config()
        self._setup_config_classes()

    def load_config(self) -> Dict[str, Any]:
        logger.info(f"Loading config from: {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _setup_config_classes(self):
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.debug = self.environment == "development"
        self.database = DatabaseConfig(self.config.get("database", {}))
        self.bot = BotConfig(self.config.get("bot", {}))
        self.fsm = FSMConfig(self.config.get("fsm", {}))
        self.locales = LocalesConfig(self.config.get("locales", {}), self.BASE_DIR)
        self.logging = LoggingConfig(self.config.get("logging", {}))
        self.redis = RedisConfig(self.config.get("redis", {}))

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value


config = Config()