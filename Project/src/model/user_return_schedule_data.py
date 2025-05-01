import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class UserReturnScheduleData:
    name_medication: str
    first_day: datetime
    last_day: datetime | None
    daily_schedule: str | List[str] = field(default_factory=list)


    def __post_init__(self):
        if isinstance(self.daily_schedule, str):
            try:
                self.daily_schedule = json.loads(self.daily_schedule)
            except json.JSONDecodeError:
                self.daily_schedule = []

    def to_dict(self) -> dict:
        try:
            schedule = json.loads(self.daily_schedule)
        except Exception as e:
            raise e

        return {
            "name_medication": self.name_medication,
            "first_day": self.first_day.strftime("%Y-%m-%d"),
            "last_day": self.last_day.strftime("%Y-%m-%d") if self.last_day else None,
            "daily_schedule": schedule,
        }
