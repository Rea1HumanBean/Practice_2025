from abc import ABC, abstractmethod
from datetime import datetime
from src.model import UserReturnScheduleData


class BaseRepository(ABC):
    @abstractmethod
    async def add_schedule_taking_medication(
        self,
        user_id: int,
        name_pills: str,
        first_day: datetime,
        last_day: datetime | None,
        daily_schedule_str: str,
    ) -> None:
        pass

    @abstractmethod
    async def get_user_schedule(
        self, user_id: int, schedule_id: int
    ) -> UserReturnScheduleData | None:
        pass

    @abstractmethod
    async def get_user_next_takings(self, user_id: int) -> list[UserReturnScheduleData]:
        pass

    @abstractmethod
    async def get_user_all_schedule_id(self, user_id: int) -> list[int] | None:
        pass
