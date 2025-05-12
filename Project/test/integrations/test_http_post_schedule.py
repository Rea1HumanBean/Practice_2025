import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

from src.create_http_server import create_http_server
from src.db_service import MedicationSchedule
from src.utils import RepositoryProvider

app = create_http_server()
client = TestClient(app)


@pytest.fixture
def mock_schedule_service():
    mock_service = AsyncMock(spec=MedicationSchedule)
    mock_service.add_schedule_taking_medication = AsyncMock()
    return mock_service


@pytest.fixture
def override_dependency(mock_schedule_service):
    def override_get_instance():
        return mock_schedule_service

    app.dependency_overrides[RepositoryProvider.get_instance] = override_get_instance
    yield
    app.dependency_overrides.clear()


def test_create_user_schedule_success(override_dependency, mock_schedule_service):
    test_data = {
        "user_id": 123,
        "name_pills": "Novokain",
        "limitation_days": 7,
        "number_iters": 3
    }

    response = client.post("/schedule", json=test_data)

    assert response.status_code == 201
    assert response.json() == {"message": "Schedule created successfully"}


    mock_schedule_service.add_schedule_taking_medication.assert_awaited_once()
    args = mock_schedule_service.add_schedule_taking_medication.call_args[1]
    assert args["user_id"] == 123