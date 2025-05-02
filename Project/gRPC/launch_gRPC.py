import asyncio
from grpc import aio
import schedule_pb2
import schedule_pb2_grpc

from src.logger import get_logger

class ScheduleService(schedule_pb2_grpc.ScheduleServiceServicer):
    async def AddSchedule(self, request, context):
        get_logger().info({
            f"AddSchedule: {request.data}"
        })
        return schedule_pb2.ScheduleResponse(success=True, error="")

    async def GetSchedule(self, request, context):
        return schedule_pb2.GetScheduleResponse(
            schedule=schedule_pb2.UserReturnScheduleData(
                name_medication="Aspirin",
                first_day="2025-05-01",
                last_day="2025-05-10",
                daily_schedule=["08:00", "20:00"]
            )
        )

    async def GetSchedules(self, request, context):
        return schedule_pb2.GetSchedulesResponse(schedules=[])

    async def GetNextTakings(self, request, context):
        return schedule_pb2.NextTakingsResponse(next_takings=[])

async def serve():
    server = aio.server()
    schedule_pb2_grpc.add_ScheduleServiceServicer_to_server(ScheduleService(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    get_logger().info({
        "Server started on port 50051"
    })
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())