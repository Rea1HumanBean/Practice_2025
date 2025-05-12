from datetime import datetime, timedelta, time

from src.model.user_return_schedule_data import UserReturnScheduleData
from src.logger import get_logger


class Services:
    @staticmethod
    def get_daily_schedule(quantity_iters: int) -> list[time]:
        START_TIME = datetime.strptime("08:00", "%H:%M")
        END_TIME = datetime.strptime("22:00", "%H:%M")

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
    def actual_schedule(
        user_list_data: list[UserReturnScheduleData] | None, time_period_hours: int
    ) -> list[str] | None:

        if user_list_data is None:
            return None

        date_now = datetime.now()

        actual_medication: list[str] = [
            user_data.name_pills
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
        daily_schedule: list[str] | str, date_now: datetime, time_period_hours: int
    ) -> bool:

        daily_schedule = Services._ensure_schedule_list(daily_schedule)
        if not daily_schedule:
            return False

        try:
            schedule_times = [
                (datetime.strptime(time_str.strip(), "%H:%M").time())
                for time_str in daily_schedule
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
            get_logger().error(
                {
                    "event": "_is_next",
                    "error": str(e),
                }
            )
            return False

    @staticmethod
    def _ensure_schedule_list(schedule_input: list[str] | str) -> list[str]:
        if isinstance(schedule_input, str):
            schedule_input = schedule_input.strip("[]'\"")
            return [t.strip(" '\"") for t in schedule_input.split(",") if t.strip()]
        return schedule_input if isinstance(schedule_input, list) else []
