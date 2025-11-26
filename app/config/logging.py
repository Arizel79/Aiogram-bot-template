import sys
from pathlib import Path

from loguru import logger

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def setup_logging():
    logger.remove()

    console_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    file_format = (
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level: <8} | "
        "{name}:{function}:{line} | "
        "{message}"
    )

    logger.add(
        sys.stderr,
        format=console_format,
        level="INFO",
        colorize=True,
        backtrace=True,
        diagnose=True,
    )

    logger.add(
        LOG_DIR / "bot.log",
        format=file_format,
        level="DEBUG",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        backtrace=True,
        diagnose=True,
    )

    logger.add(
        LOG_DIR / "errors.log",
        format=file_format,
        level="ERROR",
        rotation="5 MB",
        retention="90 days",
        compression="zip",
        backtrace=True,
        diagnose=True,
    )

    logger.add(
        LOG_DIR / "database.log",
        format=file_format,
        level="DEBUG",
        filter=lambda record: "database" in record["name"].lower(),
        rotation="5 MB",
        retention="30 days",
        compression="zip",
    )

    return logger


app_logger = setup_logging()


def get_logger(name):
    return app_logger.bind(name=name)


def get_bot_logger():
    return get_logger("bot")


def get_database_logger():
    return get_logger("db")


def get_session_logger():
    return get_logger("session")


def get_handler_logger(handler_name):
    return get_logger(f"handler.{handler_name}")


def get_middleware_logger(middleware_name):
    return get_logger(f"middleware.{middleware_name}")
