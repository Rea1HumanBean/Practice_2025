from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime


from src.db_service import BaseRepository
from src.model import UserReturnScheduleData
from src.db_service.db import Base
from src.logger import get_logger


class UserMedication(Base):
    __tablename__ = "users_medication"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    medication_name = Column(String)
    first_day = Column(DateTime)
    last_day = Column(DateTime, nullable=True)
    daily_schedule = Column(String)

class PostgreSQLScheduleRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_schedule_taking_medication(
        self,
        user_id: int,
        medication_name: str,
        first_day: datetime,
        last_day: datetime | None,
        daily_schedule_str: str,
    ) -> None:
        try:
            new_schedule = UserMedication(
                user_id=user_id,
                medication_name=medication_name,
                first_day=first_day,
                last_day=last_day,
                daily_schedule=daily_schedule_str,
            )

            self.session.add(new_schedule)
            await self.session.commit()

        except Exception as e:
            get_logger().error(
                {
                    "event": "add_schedule_taking_medication",
                    "exception": str(e),
                }
            )
            await self.session.rollback()
            raise

    async def get_user_schedule(
        self, user_id: int, schedule_id: int
    ) -> UserReturnScheduleData | None:
        try:
            result = await self.session.execute(
                select(UserMedication).where(
                    UserMedication.id == schedule_id,
                    UserMedication.user_id == user_id,
                )
            )
            row = result.scalars().first()

            if row is None:
                return None

            return UserReturnScheduleData(
                name_pills=row.med_name,
                daily_schedule=row.schedule,
                first_day=row.start_day,
                last_day=row.end_day
            )

        except Exception as e:
            get_logger().error(
                {
                    "event": "get_user_schedule",
                    "exception": str(e),
                }
            )
            raise

    async def get_user_all_schedule_id(self, user_id: int) -> list[int]:
        try:
            result = await self.session.execute(
                select(UserMedication.id).where(UserMedication.user_id == user_id)
            )

            return [row.id for row in result]
        except Exception as e:
            get_logger().error(
                {
                    "event": "get_user_all_schedule_id",
                    "exception": str(e),
                }
            )
            raise e

    async def get_user_next_takings(self, user_id: int) -> list[UserReturnScheduleData]:
        try:
            result = await self.session.execute(
                select(UserMedication).where(UserMedication.user_id == user_id)
            )
            schedules = result.scalars().all()
            result_data = [
                UserReturnScheduleData(
                    name_pills=row.medication_name,
                    daily_schedule=row.daily_schedule,
                    first_day=row.first_day,
                    last_day=row.last_day,
                )
                for row in schedules
            ]
            return result_data
        except Exception as e:
            get_logger().error(
                {
                    "event": "get_user_next_takings",
                    "exception": str(e),
                }
            )
            raise e
