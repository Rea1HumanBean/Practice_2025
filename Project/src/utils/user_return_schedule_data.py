import json
from dataclasses import dataclass, field
from typing import List


@dataclass
class UserReturnScheduleData:
    name_medication: str
    first_day: List[str]
    last_day: str
    daily_schedule: List[str] = None

    def __post_init__(self):
        if isinstance(self.daily_schedule, str):
            try:
                self.daily_schedule = json.loads(self.daily_schedule)
            except json.JSONDecodeError:
                self.daily_schedule = []
