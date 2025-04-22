from typing import Tuple
import random

from data.data import NAME, SECOND_NAME, DEPARTMENT
from model.model_Developer import Developer


class DevelopersData:
    @staticmethod
    def get_random_dev() -> Developer:
        data_dev = Developer(
            full_name=DevelopersData._rand_full_name(),
            department=DevelopersData._rand_department(),
            geolocation=DevelopersData._rand_geolocation(),
            last_known_ip=DevelopersData._rand_last_known_ip(),
            is_available=DevelopersData._rand_available()
        )
        return data_dev

    @staticmethod
    def _rand_full_name() -> str:
        rand_name: str = random.choice(NAME)
        rand_second_name: str = random.choice(SECOND_NAME)
        return f'{rand_name} {rand_second_name}'

    @staticmethod
    def _rand_department() -> str:
        rand_department: str = random.choice(DEPARTMENT)
        return rand_department

    @staticmethod
    def _rand_geolocation() -> Tuple[float, float]:
        rand_lat: float = random.uniform(-90, 90)
        rand_lon: float = random.uniform(-180, 180)
        return rand_lat, rand_lon

    @staticmethod
    def _rand_last_known_ip() -> str:
        return (f'{random.randint(1, 255)}.{random.randint(0, 255)}.'
                f'{random.randint(0, 255)}.{random.randint(1, 254)}')

    @staticmethod
    def _rand_available() -> bool:
        return bool(random.getrandbits(1))
