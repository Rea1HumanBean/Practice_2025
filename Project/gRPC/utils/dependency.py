from src.utils import RepositoryProvider
from src.db_service import PostgreSQLScheduleRepository, SessionLocal


class Dependency:
    def __init__(self):
        self._repo = None
        self._service_provider = None

    async def initialize(self):
        self._repo = PostgreSQLScheduleRepository(SessionLocal())
        self._service_provider = await RepositoryProvider.get_instance()

    @property
    def schedule_service(self):
        if self._service_provider is None:
            raise RuntimeError("Dependencies not initialized")
        return self._service_provider
