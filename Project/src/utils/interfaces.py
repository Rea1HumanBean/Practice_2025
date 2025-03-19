from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime, time
from .user_return_schedule_data import UserReturnScheduleData


class IMedicationRepository(ABC):
    @abstractmethod
    def add_schedule_taking_medication(
        self,
        user_id: int,
        name_pills: str,
        first_day: datetime,
        last_day: Optional[datetime],
        daily_schedule: list[time],
    ) -> None:
        pass

    @abstractmethod
    def get_user_schedule(
        self, user_id: int, schedule_id: int
    ) -> Optional[UserReturnScheduleData]:
        pass

    @abstractmethod
    def get_user_next_takings(self, user_id: int) -> List[UserReturnScheduleData]:
        pass

    @abstractmethod
    def get_user_id_schedule(self, user_id: int) -> int | None:
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> bool:
        pass
