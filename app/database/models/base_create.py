from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from app.core import settings


class Base(AsyncAttrs, DeclarativeBase):
    pass

engine = create_async_engine(
    url=settings.DATABASE_URL.get_secret_value(),
    echo=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=True,
    class_=AsyncSession
)