import grpc
from gRPC import schedule_pb2, schedule_pb2_grpc

from gRPC.utils.validate_id import validate_grpc_id
from src.config import TIME_PERIOD_HOURS
from src.model import ScheduleDateService
from src.logger import get_logger
from src.services import Services
from gRPC.models import DataOfUserRequest, UserReturnScheduleData


class ScheduleService(schedule_pb2_grpc.ScheduleServiceServicer):
    def __init__(self, service_provider):
        self.service = service_provider

    async def AddSchedule(self, request, context):
        try:
            user_data = DataOfUserRequest(
                user_id=request.data.user_id,
                name_pills=request.data.name_pills,
                limitation_days=request.data.limitation_days,
                number_iters=request.data.number_iters
            )

            schedule_data = ScheduleDateService(
                limitation_days=user_data.limitation_days,
                daily_iterations=user_data.number_iters,
            )

            await self.service.add_schedule_taking_medication(
                user_id=user_data.user_id,
                name_pills=user_data.name_pills,
                first_day=schedule_data.first_day,
                last_day=schedule_data.last_day,
                daily_schedule=schedule_data.daily_schedule,
            )

            return schedule_pb2.ScheduleResponse(
                success=True,
                message="Schedule creation completed successfully"
            )

        except ValueError as e:
            get_logger().error(f"Data validation error: {str(e)}")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Invalid request data: {str(e)}")
            return schedule_pb2.ScheduleResponse(
                success=False,
                message="Schedule creation failed"
            )


        except Exception as e:
            get_logger().error(f"Schedule creation failed: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Schedule creation failed")
            return schedule_pb2.ScheduleResponse(
                success=False,
                message="Schedule creation failed"
            )

    async def GetSchedule(self, request, context):
        try:

            user_data = {
                "user_id": validate_grpc_id(request.user_id),
                "schedule_id": validate_grpc_id(request.schedule_id)
            }

            result = await self.service.get_user_schedule(
                user_data["user_id"],
                user_data["schedule_id"]
            )

            if not result:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return schedule_pb2.GetScheduleResponse()

            return UserReturnScheduleData(
                schedule=schedule_pb2.UserReturnScheduleData(
                    name_medication=result.name_medication,
                    first_day=result.first_day,
                    last_day=result.last_day,
                    daily_schedule=result.daily_schedule
                )
            )

        except ValueError as e:
            get_logger().error(f"ID validation error: {str(e)}")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Invalid ID: {str(e)}")
            return schedule_pb2.GetScheduleResponse()

        except Exception as e:
            get_logger().error(f"Get schedule failed: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return schedule_pb2.GetScheduleResponse()

    async def GetSchedules(self, request, context) -> schedule_pb2.GetSchedulesResponse:
        try:
            user_id = request.user_id
            user_schedule_id: list[int] | None = (
                await self.service.get_user_all_schedule_id(user_id)
            )

            get_logger().debug({"event": "get_schedules", "data": user_schedule_id})

            if user_schedule_id is not None:
                return schedule_pb2.GetSchedulesResponse(status_code=200, content=user_schedule_id)
            else:
                return schedule_pb2.GetSchedulesResponse(
                    status_code=400, content={"error": "Missing required fields"}
                )
        except ValueError as e:
            get_logger().error({"event": "id_validation", "error": str(e)})
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return schedule_pb2.GetScheduleResponse()

        except Exception as e:
            get_logger().error({"event": "get_schedules", "error": str(e)})
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return schedule_pb2.GetScheduleResponse()

    async def GetNextTakings(self, request, context) -> schedule_pb2.NextTakingsResponse:
        try:
            user_id: int = validate_grpc_id(request.user_id)

            medications: list[UserReturnScheduleData] = await self.service.get_user_next_takings(user_id)

            upcoming_meds: list[str] = Services.actual_schedule(
                medications, TIME_PERIOD_HOURS
            )

            get_logger().debug(
                {"event": "next_takings_result", "actual_medication": upcoming_meds}
            )

            return schedule_pb2.NextTakingsResponse(
                next_takings=upcoming_meds
            )

        except ValueError as e:
            get_logger().error({"event": "id_validation", "error": str(e)})
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return schedule_pb2.NextTakingsResponse()

        except Exception as e:
            get_logger().error({"event": "next_takings", "error": str(e)})
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return schedule_pb2.NextTakingsResponse()
