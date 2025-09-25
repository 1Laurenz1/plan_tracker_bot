from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import joinedload

from datetime import datetime
import calendar

from app.database import (
    AsyncSessionLocal,
    User,
    Schedule,
    ScheduleItem
)
from app.core import logger

from typing import (
    List,
    Dict,
    Optional,
    Union
)


class ScheduleRepository:
    def __init__(self):
        pass
    
    async def create_schedule(
        self,
        user_id: int,
        name: str,
        schedule_type: str
    ) -> Optional[Schedule]:
        async with AsyncSessionLocal() as session:
            try:
                user = await session.execute(
                    select(User).filter_by(user_id=user_id)
                )
                user = user.scalar_one_or_none()

                if user is None:
                    logger.error(f"User with user_id {user_id} does not exist. Cannot create schedule.")
                    return None

                new_schedule = Schedule(
                    user_id=user_id,
                    name=name,
                    type=schedule_type
                )

                session.add(new_schedule)
                await session.commit()
                await session.refresh(new_schedule)

                logger.info(f"Created new schedule '{name}' for user {user_id}")

                return new_schedule
            except IntegrityError as e:
                await session.rollback()
                logger.error(f"Integrity error while creating schedule '{name}' for user {user_id}: {e}")
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"DB error while creating schedule '{name}' for user {user_id}: {e}")

        return None
    
    
    async def add_item_in_schedule(
        self,
        user_id: int,
        schedule_id: int,
        items: List[Dict]
    ) -> bool:
        async with AsyncSessionLocal() as session:
            try:
                exists_schedule_id = await session.execute(
                    select(Schedule).
                    where(Schedule.id == schedule_id)
                )
                
                if not exists_schedule_id:
                    return None
                
                schedule_items = [
                    ScheduleItem(
                        schedule_id=schedule_id,
                        title=item.get("title"),
                        description=item.get("description"),
                        day_of_week=item.get("day_of_week"),
                        time_start=item.get("time_start"),
                        time_end=item.get("time_end"),
                    )
                    for item in items
                ]
                    
                session.add_all(schedule_items)
                await session.commit()
                
                for item in schedule_items:
                    await session.refresh(item)
                    
                logger.info(f"{len(items)} items added to schedule {schedule_id}")
                
                return True
                
            except IntegrityError as e:
                await session.rollback()
                logger.error(
                    f"Integrity error while adding items {schedule_items} "
                    f"in schedule_id '{schedule_id}' for user {user_id}: {e}"
                )
                return None
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(
                    f"DB error while adding items: {schedule_items} "
                    f"in schedule_id '{schedule_id}' for user {user_id}: {e}"
                )
                return None
        return False

    
    async def get_user_schedules_paginated(
        self,
        user_id: int,
        page: int
    ) -> tuple[list[Schedule], bool]:
        schedules_on_page = 5
        offset = page * schedules_on_page

        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(
                    select(Schedule)
                    .where(Schedule.user_id == user_id)
                    .order_by(Schedule.created_at.desc())
                    .offset(offset)
                    .limit(schedules_on_page + 1)
                )

                schedules = result.scalars().all()

                has_next = len(schedules) > schedules_on_page
                return schedules[:schedules_on_page], has_next

            except IntegrityError as e:
                await session.rollback()
                logger.error(f"Integrity error while fetching schedules for user {user_id}: {e}")
                return [], False
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"DB error while fetching schedules for user {user_id}: {e}")
                return [], False
    
    

    async def check_schedule_type(
        self,
        user_id: int,
        schedule_id: int,
        schedule_types: List[str]
    ) -> Optional[Schedule]:
        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(
                    select(Schedule).where(
                        Schedule.user_id == user_id,
                        Schedule.id == schedule_id,
                        Schedule.type.in_(schedule_types)
                    )
                )
                
                return result.scalar_one_or_none()
            
            except IntegrityError as e:
                await session.rollback()
                logger.error(f"Integrity error while checking schedule for user {user_id}: {e}")
                return None
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"DB error while checking schedule for user {user_id}: {e}")
                return None
    
    
class ScheduleItemsRepository:
    def __init__(self):
        pass
    
    
    async def check_today_schedule(
        self,
        user_id,
    ) -> Optional[ScheduleItem]:
        today = datetime.today().strftime("%A").upper()
        
        async with AsyncSessionLocal() as session:
            try:
                exists_items_schedule_id = await session.execute(
                    select(ScheduleItem)
                    .join(Schedule)
                    .where(
                        Schedule.user_id == user_id,
                        ScheduleItem.day_of_week == today
                    )
                )
                
                items = exists_items_schedule_id.scalars().all()
                
                if not items:
                    return None
                
                return items
            except IntegrityError as e:
                await session.rollback()
                logger.error(f"Integrity error while checking today schedule for user {user_id}: {e}")
                return None
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"DB error while checking today schedule for user {user_id}: {e}")
                return None
    
    
    async def check_schedule_for_the_week(
        self,
        user_id
    ) -> List[ScheduleItem]:
        week_days = [day.upper() for day in calendar.day_name]
        
        async with AsyncSessionLocal() as session:
            try:
                exists_items_schedule_id = await session.execute(
                    select(ScheduleItem)
                    .join(Schedule)
                    .where(
                        Schedule.user_id == user_id,
                        ScheduleItem.day_of_week.in_(week_days)
                    )
                )
                
                items = exists_items_schedule_id.scalars().all()
                
                if not items:
                    return None

                return items
            except IntegrityError as e:
                await session.rollback()
                logger.error(f"Integrity error while checking for the week schedules for user {user_id}: {e}")
                return []
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"DB error while checking for the week schedules for user {user_id}: {e}")
                return []
    
    
schedule_repos = ScheduleRepository()
schedule_items_repos = ScheduleItemsRepository()