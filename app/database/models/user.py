from sqlalchemy import (
    String,
    Integer,
    BigInteger,
    ForeignKey,
    DateTime,
    func,
    BIGINT
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from .base_create import Base

from datetime import datetime


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    user_id: Mapped[BIGINT] = mapped_column(
        BigInteger,
        nullable=False,
        unique=True,
        index=True
    )
    username: Mapped[str] = mapped_column(
        String(32),
        nullable=True,
        unique=False
    )
    first_name: Mapped[str] = mapped_column(
        String(32),
        nullable=True,
        unique=False
    )
    last_name: Mapped[str] = mapped_column(
        String(32),
        nullable=True,
        unique=False
    )
    timezone: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        unique=False,
        server_default="UTC"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )