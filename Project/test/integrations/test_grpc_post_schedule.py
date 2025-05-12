import grpc
from unittest.mock import AsyncMock, MagicMock, ANY

import pytest
import pytest_asyncio

from gRPC import schedule_pb2, schedule_pb2_grpc
from gRPC.schedule_grpc_service import ScheduleService


@pytest.fixture
def mock_schedule_service():
    mock = MagicMock()
    mock.add_schedule_taking_medication = AsyncMock(
        return_value=schedule_pb2.ScheduleResponse(
            success=True,
            message="Schedule creation completed successfully"
        )
    )
    return mock

@pytest_asyncio.fixture
async def grpc_server(mock_schedule_service):
    server = grpc.aio.server()
    schedule_pb2_grpc.add_ScheduleServiceServicer_to_server(
        ScheduleService(mock_schedule_service),
        server
    )
    server.add_insecure_port('[::]:50051')
    await server.start()
    yield server
    await server.stop(0)

@pytest_asyncio.fixture
async def grpc_channel(grpc_server):
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        yield channel


@pytest.mark.asyncio
async def test_add_schedule_success(mock_schedule_service, grpc_channel):
    stub = schedule_pb2_grpc.ScheduleServiceStub(grpc_channel)

    mock_response = schedule_pb2.ScheduleResponse(
        success=True,
        message="Schedule creation completed successfully"
    )
    mock_schedule_service.add_schedule_taking_medication.return_value = mock_response

    request = schedule_pb2.ScheduleRequest(
        data=schedule_pb2.DataOfUserRequest(
            user_id=123,
            name_pills="Novokain",
            limitation_days=7,
            number_iters=3
        )
    )

    response = await stub.AddSchedule(request)

    assert response.success is True
    assert "Schedule creation completed successfully" in response.message
    mock_schedule_service.add_schedule_taking_medication.assert_awaited_once_with(
        user_id=123,
        name_pills="Novokain",
        first_day=ANY,
        last_day=ANY,
        daily_schedule=ANY
    )
