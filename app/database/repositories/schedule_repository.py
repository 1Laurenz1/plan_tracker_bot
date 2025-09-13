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
    ) -> Optional[Schedule]:
        async with AsyncSessionLocal() as session:
            try:
                new_schedule = Schedule(
                    user_id=user_id,
                    name=name
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