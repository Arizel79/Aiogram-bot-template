from decimal import Decimal

from sqlalchemy import (
    String,
    Integer,
    BigInteger,
    func, Numeric,
)

from app.config import config
from app.db.models.shared import *


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, unique=True, index=True, nullable=False, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)

    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)

    language = Column(String(2), default=config.locales.default_locale)
    balance = Column(Numeric(10, 2), nullable=True, default=Decimal("0"))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
