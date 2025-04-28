import json
from typing import List
from datetime import datetime
import logging

from src.utils.interfaces import IMedicationRepository
from src.utils.user_return_schedule_data import UserReturnScheduleData


class MedicationSchedule:
    def __init__(self, repository: IMedicationRepository):
        self.repository = repository

    async def add_schedule_taking_medication(
        self,
        user_id: int,
        name_pills: str,
        first_day: datetime,
        last_day: datetime,
        daily_schedule: str,
    ) -> None:
        try:
            daily_schedule_str = json.dumps(daily_schedule, default=str)

            await self.repository.add_schedule_taking_medication(
                user_id, name_pills, first_day, last_day, daily_schedule_str)
        except Exception as e:
            logging.exception(e)

    async def get_user_all_schedule_id(self, user_id: int) -> List[int] | None:
        return await self.repository.get_user_all_schedule_id(user_id)

    async def get_user_schedule(
        self, user_id: int, schedule_id: int
    ) -> UserReturnScheduleData | None:
        return await self.repository.get_user_schedule(user_id, schedule_id)

    async def get_user_next_takings(self, user_id: int) -> List[UserReturnScheduleData] | None:
        return await self.repository.get_user_next_takings(user_id)
