import json
from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserReturnScheduleData:
    name_pills: str
    first_day: datetime
    last_day: datetime | None
    daily_schedule: list[str]

    def __post_init__(self):
        if isinstance(self.daily_schedule, str):
            try:
                self.daily_schedule = json.loads(self.daily_schedule)
            except json.JSONDecodeError:
                self.daily_schedule = []

    def to_dict(self) -> dict:
        return {
            "name_medication": self.name_pills,
            "first_day": self.first_day.strftime("%Y-%m-%d"),
            "last_day": self.last_day.strftime("%Y-%m-%d") if self.last_day else None,
            "daily_schedule": self.daily_schedule,
        }
