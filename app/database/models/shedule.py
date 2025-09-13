import enum
from datetime import datetime, time

from sqlalchemy import (
    String,
    Integer,
    BigInteger,
    ForeignKey,
    DateTime,
    Time,
    Boolean,
    Enum as SQLEnum,
    func
)
from sqlalchemy.orm import Mapped, mapped_column

from .base_create import Base
from .user import User


class ScheduleType(enum.Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"


class DayOfWeek(enum.Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"


class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            f"{User.__tablename__}.user_id"   
        ),
        nullable=False
    )
    name: Mapped[str] = mapped_column(
        String(64),
        nullable=False
    )
    type: Mapped[ScheduleType] = mapped_column(
        SQLEnum(ScheduleType, name="scheduletype"),
        nullable=False,
        server_default="DAILY"
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


class ScheduleItem(Base):
    __tablename__ = "schedule_items"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    schedule_id: Mapped[int] = mapped_column(
        ForeignKey("schedules.id"),
        nullable=False
    )
    title: Mapped[str] = mapped_column(
        String(128),
        nullable=True
    )
    description: Mapped[str] = mapped_column(
        String(256),
        nullable=True
    )
    day_of_week: Mapped[DayOfWeek] = mapped_column(
        SQLEnum(DayOfWeek, name="day_of_week_enum"),
        nullable=False
    )
    time_start: Mapped[time] = mapped_column(
        Time,
        nullable=False
    )
    time_end: Mapped[time] = mapped_column(
        Time,
        nullable=False
    )
    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False
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
