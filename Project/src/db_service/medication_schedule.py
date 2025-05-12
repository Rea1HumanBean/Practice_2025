import json
from typing import List
from datetime import datetime

from src.logger import trace_id_var, get_logger
from src.db_service.base_repository import BaseRepository
from src.model import UserReturnScheduleData


class MedicationSchedule:
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    async def add_schedule_taking_medication(
        self,
        user_id: int,
        name_pills: str,
        first_day: datetime,
        last_day: datetime | None,
        daily_schedule: str,
    ) -> None:

        get_logger().debug(
            {
                "event": "add_schedule_taking_medication_start",
                "trace_id": trace_id_var,
                "user_id": user_id,
                "med_name": name_pills,
                "first_day": first_day.isoformat(),
                "last_day": last_day.isoformat() if last_day else None,
                "daily_schedule": daily_schedule,
            }
        )
        try:
            daily_schedule_str = json.dumps(daily_schedule, default=str)

            await self.repository.add_schedule_taking_medication(
                user_id, name_pills, first_day, last_day, daily_schedule_str
            )

        except Exception as e:
            get_logger().exception(
                {
                    "event": "add_schedule_taking_medication_error",
                    "trace_id": trace_id_var,
                    "error": str(e),
                }
            )

    async def get_user_all_schedule_id(self, user_id: int) -> List[int] | None:
        return await self.repository.get_user_all_schedule_id(user_id)

    async def get_user_schedule(
        self, user_id: int, schedule_id: int
    ) -> UserReturnScheduleData | None:
        return await self.repository.get_user_schedule(user_id, schedule_id)

    async def get_user_next_takings(
        self, user_id: int
    ) -> List[UserReturnScheduleData] | None:
        return await self.repository.get_user_next_takings(user_id)

