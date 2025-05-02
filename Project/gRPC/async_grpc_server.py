from datetime import datetime
from typing import List
import json
import grpc
from grpc import StatusCode
import schedule_pb2
import schedule_pb2_grpc
from src.config import TIME_PERIOD_HOURS
from src.model import ScheduleDateService
from src.services import Services
from src.logger import get_logger

class AsyncScheduleService(schedule_pb2_grpc.ScheduleServiceServicer):
    def __init__(self, schedule_service):
        self.schedule_service = schedule_service
        self.logger = get_logger()

    async def _log_error(self, method_name: str, error: Exception, context):
        self.logger.error({
            "event": f"grpc_{method_name}_error",
            "error": str(error),
            "trace_id": context.invocation_metadata().get('x-trace-id', '')
        })

    async def AddSchedule(self, request, context):
        try:
            self.logger.debug(f"AddSchedule request: {request}")

            user_data = request.data
            schedule_data = ScheduleDateService(
                limitation_days=user_data.limitation_days,
                daily_iterations=user_data.number_iters,
            )

            await self.schedule_service.add_schedule_taking_medication(
                user_id=user_data.user_id,
                name_pills=user_data.name_pills,
                first_day=schedule_data.first_day,
                last_day=schedule_data.last_day,
                daily_schedule=json.dumps(schedule_data.daily_schedule),
            )

            return schedule_pb2.ScheduleResponse(success=True, error="")

        except ValueError as e:
            await self._log_error("AddSchedule", e, context)
            await context.abort(StatusCode.INVALID_ARGUMENT, str(e))
        except Exception as e:
            await self._log_error("AddSchedule", e, context)
            await context.abort(StatusCode.INTERNAL, "Internal server error")

    async def GetSchedules(self, request, context):
        try:
            self.logger.debug(f"GetSchedules request: {request}")

            user_id = request.user_id
            schedule_ids = await self.schedule_service.get_user_all_schedule_id(user_id)

            if not schedule_ids:
                await context.abort(StatusCode.NOT_FOUND, "No schedules found")

            # Получаем полные данные о расписаниях
            schedules = []
            for schedule_id in schedule_ids:
                schedule = await self.schedule_service.get_user_schedule(user_id, schedule_id)
                if schedule:
                    schedules.append(schedule_pb2.UserReturnScheduleData(
                        name_medication=schedule.name_medication,
                        first_day=schedule.first_day.isoformat(),
                        last_day=schedule.last_day.isoformat() if schedule.last_day else "",
                        daily_schedule=schedule.daily_schedule if isinstance(schedule.daily_schedule, list)
                        else json.loads(schedule.daily_schedule)
                    ))

            return schedule_pb2.GetSchedulesResponse(schedules=schedules)

        except Exception as e:
            await self._log_error("GetSchedules", e, context)
            await context.abort(StatusCode.INTERNAL, "Internal server error")

    async def GetSchedule(self, request, context):
        try:
            self.logger.debug(f"GetSchedule request: {request}")

            schedule = await self.schedule_service.get_user_schedule(
                request.user_id, request.schedule_id
            )

            if not schedule:
                await context.abort(StatusCode.NOT_FOUND, "Schedule not found")

            return schedule_pb2.GetScheduleResponse(
                schedule=schedule_pb2.UserReturnScheduleData(
                    name_medication=schedule.name_medication,
                    first_day=schedule.first_day.isoformat(),
                    last_day=schedule.last_day.isoformat() if schedule.last_day else "",
                    daily_schedule=schedule.daily_schedule if isinstance(schedule.daily_schedule, list)
                    else json.loads(schedule.daily_schedule)
                )
            )
        except Exception as e:
            await self._log_error("GetSchedule", e, context)
            await context.abort(StatusCode.INTERNAL, "Internal server error")

    async def GetNextTakings(self, request, context):
        try:
            self.logger.debug(f"GetNextTakings request: {request}")

            schedules = await self.schedule_service.get_user_next_takings(request.user_id)
            if not schedules:
                await context.abort(StatusCode.NOT_FOUND, "No schedules found")

            actual_meds = Services.check_actual_schedule(schedules, TIME_PERIOD_HOURS)

            return schedule_pb2.NextTakingsResponse(
                next_takings=[
                    schedule_pb2.ReturnUserActualSchedule(
                        name_medication=med,
                        next_time=datetime.now().isoformat()
                    ) for med in actual_meds
                ]
            )
        except Exception as e:
            await self._log_error("GetNextTakings", e, context)
            await context.abort(StatusCode.INTERNAL, "Internal server error")