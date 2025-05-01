import json
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class ScheduleDateService:
    limitation_days: int | None
    daily_iterations: int
    first_day: datetime = field(init=False)
    last_day: datetime | None = field(init=False)
    daily_schedule: str = field(init=False)

    def __post_init__(self) -> None:
        from src.services.services import Services

        arr_daily_schedule = Services.get_daily_schedule(self.daily_iterations)
        self.daily_schedule = json.dumps([t.strftime("%H:%M") for t in arr_daily_schedule])
        self.first_day = Services.get_today()
        self.last_day = Services.get_last_day(self.limitation_days)
