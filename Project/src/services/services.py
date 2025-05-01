import json
import logging
from datetime import datetime, timedelta, time
from typing import List
from src.model.user_return_schedule_data import UserReturnScheduleData


class Services:
    @staticmethod
    def get_daily_schedule(quantity_iters: int) -> list[time]:
        START_TIME = datetime.strptime("08:00", "%H:%M")
        END_TIME = datetime.strptime("22:00", "%H:%M")

        if quantity_iters < 1:
            raise ValueError("quantity_iters cannot be less than 1")

        if quantity_iters == 1:
            return [START_TIME.time()]

        interval = (END_TIME - START_TIME) / (quantity_iters - 1)

        schedule = [
            Services._round_time(START_TIME + i * interval).time()
            for i in range(quantity_iters)
        ]
        return schedule

    @staticmethod
    def _round_time(time_obj: datetime) -> datetime:
        minutes = time_obj.minute
        new_minutes = (minutes // 15 + 1) * 15 if minutes % 15 else minutes
        return (
            time_obj.replace(minute=new_minutes)
            if new_minutes != 60
            else time_obj.replace(hour=time_obj.hour + 1, minute=0)
        )

    @staticmethod
    def get_today() -> datetime:
        return datetime.today()

    @staticmethod
    def get_last_day(last_day: int | None) -> datetime | None:
        if last_day is None:
            return None
        return datetime.today() + timedelta(days=last_day)

    @staticmethod
    def check_actual_schedule(
        user_list_data: List[UserReturnScheduleData], time_period_hours: int
    ) -> List[str | None]:

        if user_list_data is None:
            return []

        date_now = datetime.now()

        actual_medication: List[str | None] = [
            user_data.name_medication
            for user_data in user_list_data
            if Services._is_valid_schedule(user_data, date_now, time_period_hours)
        ]
        return actual_medication

    @staticmethod
    def _is_valid_schedule(
        user_data: UserReturnScheduleData, date_now: datetime, time_period_hours: int
    ) -> bool:
        if user_data.last_day is None:
            return Services._is_next(
                user_data.daily_schedule, date_now, time_period_hours
            )

        if date_now > user_data.last_day:
            return False

        return Services._is_next(user_data.daily_schedule, date_now, time_period_hours)

    @staticmethod
    def _is_next(
        daily_schedule: str, date_now: datetime, time_period_hours: int
    ) -> bool:
        try:
            print(daily_schedule)
            schedule_times = [
                (datetime.strptime(time_str.strip(), "%H:%M").time())
                for time_str in json.loads(daily_schedule)
            ]

            current_time = date_now.replace(microsecond=0).time()

            end_time = (
                (date_now + timedelta(hours=time_period_hours))
                .time()
                .replace(microsecond=0)
            )

            for time_iter in schedule_times:
                if current_time <= time_iter <= end_time:
                    return True

            return False
        except Exception as e:
            logging.error(e)
            return False
