from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal

from app.db.models import User
from app.config.logging import get_logger

logger = get_logger("user_service")


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_user(
        self,
        telegram_id: int,
        username: str = None,
        first_name: str = None,
        last_name: str = None,
    ) -> User:
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

        if user:
            needs_update = False
            if user.username != username:
                user.username = username
                needs_update = True
            if user.first_name != first_name:
                user.first_name = first_name
                needs_update = True
            if user.last_name != last_name:
                user.last_name = last_name
                needs_update = True

            if needs_update:
                self.session.add(user)
                await self.session.commit()
                logger.debug(f"Updated user data for {telegram_id}")
        else:
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
            )
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            logger.info(f"Created new user: {telegram_id}")

        return user

    async def update_user_language(self, user: User, language: str) -> User:
        user.language = language
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        logger.info(f"Updated language for user {user.telegram_id} to {language}")
        return user
