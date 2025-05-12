from datetime import time

from src.services import Services


class TestGetDailySchedule:

    @staticmethod
    def test_single_iteration():
        result = Services.get_daily_schedule(quantity_iters=1)
        assert result == [time(8, 0)]

    @staticmethod
    def test_two_iterations():
        result = Services.get_daily_schedule(quantity_iters=2)
        assert result == [time(8, 0), time(22, 0)]

    @staticmethod
    def test_three_iterations():
        result = Services.get_daily_schedule(quantity_iters=3)
        expected = [
            time(8, 0),
            time(15, 0),
            time(22, 0),
        ]
        assert result == expected

    @staticmethod
    def test_five_iterations():
        result = Services.get_daily_schedule(quantity_iters=5)
        expected = [
            time(8, 0),
            time(11, 30),
            time(15, 0),
            time(18, 30),
            time(22, 0),
        ]
        assert result == expected
