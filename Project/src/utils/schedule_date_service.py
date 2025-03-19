from .services import Services
from datetime import datetime, time
from dataclasses import dataclass, field


@dataclass
class ScheduleDateService:
    limitation_days: int | None
    daily_iterations: int
    first_day: datetime = field(default_factory=Services.get_today)
    last_day: datetime | None = field(init=False)
    daily_schedule: list[time] = field(init=False)

    def __post_init__(self):
        self.last_day = Services.get_last_day(self.limitation_days)
        self.daily_schedule = Services.get_daily_schedule(self.daily_iterations)
