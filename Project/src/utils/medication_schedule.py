from typing import List
from datetime import time, datetime

from .interfaces import IMedicationRepository
from .user_return_schedule_data import UserReturnScheduleData


class MedicationSchedule:
    def __init__(self, repository: IMedicationRepository):
        self.repository = repository

    def add_schedule_taking_medication(
        self,
        user_id: int,
        name_pills: str,
        first_day: datetime,
        last_day: datetime,
        daily_schedule: list[time],
    ) -> None:
        self.repository.add_schedule_taking_medication(
            user_id, name_pills, first_day, last_day, daily_schedule
        )

    def get_user_id_schedule(self, user_id: int) -> int | None:
        if self.check_user(user_id):
            return self.repository.get_user_id_schedule(user_id)
        return None

    def get_user_schedule(
        self, user_id: int, schedule_id: int
    ) -> UserReturnScheduleData | None:
        return self.repository.get_user_schedule(user_id, schedule_id)

    def get_user_next_takings(self, user_id: int) -> List[UserReturnScheduleData]:
        return self.repository.get_user_next_takings(user_id)

    def check_user(self, user_id: int) -> bool:
        return self.repository.get_user(user_id)
