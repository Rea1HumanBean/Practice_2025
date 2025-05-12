from __future__ import annotations

from src.db_service import (
    SessionLocal,
    PostgreSQLScheduleRepository,
    MedicationSchedule,
)


class RepositoryProvider:
    _instance: MedicationSchedule | None = None

    @classmethod
    async def get_instance(cls) -> MedicationSchedule:
        if cls._instance is None:
            repo = PostgreSQLScheduleRepository(SessionLocal())
            cls._instance = MedicationSchedule(repo)
        return cls._instance
