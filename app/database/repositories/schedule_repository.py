from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.database import (
    AsyncSessionLocal,
    User,
    Schedule,
    ScheduleItem
)
from app.core import logger

from typing import List, Optional, Union


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
                # Check if user exists
                user = await session.execute(
                    select(User).filter_by(user_id=user_id)
                )
                user = user.scalar_one_or_none()

                if user is None:
                    logger.error(f"User with user_id {user_id} does not exist. Cannot create schedule.")
                    return None

                # Proceed with creating the schedule
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
    

schedule_repos = ScheduleRepository()