from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
)

from app.db.base import Base


class BaseTimeModel(Base):
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.utcnow)
