from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from .user_return_schedule_data import UserReturnScheduleData


class IMedicationRepository(ABC):
    @abstractmethod
    async def add_schedule_taking_medication(
        self,
        user_id: int,
        medication_id: id,
        first_day: datetime,
        last_day: Optional[datetime],
        daily_schedule_str: str,
    ) -> None:
        pass

    @abstractmethod
    async def get_user_schedule(
        self, user_id: int, schedule_id: int
    ) -> Optional[UserReturnScheduleData]:
        pass

    @abstractmethod
    async def get_user_next_takings(self, user_id: int) -> List[UserReturnScheduleData]:
        pass

    @abstractmethod
    async def get_user_all_schedule_id(self, user_id: int) -> List[int] | None:
        pass
