import asyncio
from contextlib import suppress

from app.bot import telegram_bot
from app.config.logging import get_logger

logger = get_logger("main")


async def main():
    logger.info("Starting application...")

    try:
        await telegram_bot.start_polling()

    except Exception as e:
        logger.error(f"Application error: {e}")
        raise
    finally:
        await telegram_bot.stop()
        logger.info("Application shutdown complete")


def run():
    with suppress(KeyboardInterrupt):
        asyncio.run(main())


if __name__ == "__main__":
    run()
