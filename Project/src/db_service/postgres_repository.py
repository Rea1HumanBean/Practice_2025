from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.future import select
from datetime import datetime
from typing import List
from abc import ABC

from src.utils.interfaces import IMedicationRepository
from src.utils.user_return_schedule_data import UserReturnScheduleData
from src.db_service.db import Base


class UserMedication(Base):
    __tablename__ = "users_medication"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    medication_name = Column(String)
    first_day = Column(DateTime)
    last_day = Column(DateTime, nullable=True)
    daily_schedule = Column(String)


class PostgreSQLScheduleRepository(IMedicationRepository, ABC):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def get_session(self):
        return self.session_factory()

    async def add_schedule_taking_medication(
            self,
            user_id: int,
            medication_name: str,
            first_day: datetime,
            last_day: datetime | None,
            daily_schedule_str: str,
    ) -> None:
        async with self.session_factory() as db:
            new_schedule = UserMedication(
                user_id=user_id,
                medication_name=medication_name,
                first_day=first_day,
                last_day=last_day,
                daily_schedule=daily_schedule_str
            )
            try:
                db.add(new_schedule)
                await db.commit()
            except Exception as e:
                await db.rollback()
                raise e

    async def get_user_schedule(self, user_id: int, schedule_id: int) -> UserReturnScheduleData | None:
        async with self.session_factory() as db:
            try:
                result = await db.execute(
                    select(UserMedication)
                    .where(schedule_id == UserMedication.id, user_id == UserMedication.user_id)
                )
                row = result.scalars().first()
                print(row)

                if not result:
                    return None

                return UserReturnScheduleData(
                    name_medication=row.medication_name,
                    daily_schedule=row.daily_schedule,
                    first_day=row.first_day,
                    last_day=row.last_day,
                )
            except Exception as e:
                raise e

    async def get_user_all_schedule_id(self, user_id: int) -> List[int]:
        async with self.session_factory() as db:
            try:
                result = (
                    await db.execute(
                        select(UserMedication.id)
                        .where(user_id == UserMedication.user_id)
                        )
                )
                return [row.id for row in result]
            except Exception as e:
                raise e

    async def get_user_next_takings(self, user_id: int) -> List[UserReturnScheduleData]:
        async with self.session_factory() as db:
            try:
                result = await db.execute(
                    select(UserMedication)
                    .where(user_id == UserMedication.user_id)
                )
                schedules = result.scalars().all()
                result_data = [
                    UserReturnScheduleData(
                        name_medication=row.medication_name,
                        daily_schedule=row.daily_schedule,
                        first_day=row.first_day,
                        last_day=row.last_day,
                    )
                    for row in schedules
                ]
                return result_data
            except Exception as e:
                raise e
