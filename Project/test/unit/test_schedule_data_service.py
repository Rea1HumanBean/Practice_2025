from datetime import datetime, timedelta
from unittest.mock import patch
import json

from src.services import Services
from src.model import ScheduleDateService


class TestScheduleDateService:

    @patch.object(Services, 'get_daily_schedule')
    @patch.object(Services, 'get_today')
    @patch.object(Services, 'get_last_day')
    def test_normal_initialization(self, mock_get_last_day, mock_get_today, mock_get_daily):
        test_time = datetime(2025, 5, 12)
        mock_get_today.return_value = test_time
        mock_get_last_day.return_value = test_time + timedelta(days=7)
        mock_get_daily.return_value = [datetime.strptime("08:00", "%H:%M").time(),
                                       datetime.strptime("22:00", "%H:%M").time()]

        schedule = ScheduleDateService(
            limitation_days=7,
            daily_iterations=2
        )

        assert schedule.first_day == test_time
        assert schedule.last_day == test_time + timedelta(days=7)
        assert json.loads(schedule.daily_schedule) == ["08:00", "22:00"]

    @patch.object(Services, 'get_daily_schedule')
    @patch.object(Services, 'get_today')
    def test_no_limitation_days(self, mock_get_today, mock_get_daily):

        test_time = datetime(2025, 5, 12)
        mock_get_today.return_value = test_time
        mock_get_daily.return_value = [datetime.strptime("08:00", "%H:%M").time()]

        schedule = ScheduleDateService(
            limitation_days=None,
            daily_iterations=1
        )

        assert schedule.last_day is None
        assert schedule.first_day == test_time
        assert json.loads(schedule.daily_schedule) == ["08:00"]

    @patch.object(Services, 'get_daily_schedule')
    @patch.object(Services, 'get_today')
    def test_boundary_values(self, mock_get_today, mock_get_daily):
        mock_get_today.return_value = datetime(2025, 5, 12)
        mock_get_daily.return_value = [datetime.strptime("08:00", "%H:%M").time()]

        schedule = ScheduleDateService(
            limitation_days=1,
            daily_iterations=1
        )

        assert json.loads(schedule.daily_schedule) == ["08:00"]

    @patch.object(Services, 'get_daily_schedule')
    def test_empty_schedule(self, mock_get_daily):
        mock_get_daily.return_value = []

        schedule = ScheduleDateService(
            limitation_days=7,
            daily_iterations=0
        )

        assert json.loads(schedule.daily_schedule) == []