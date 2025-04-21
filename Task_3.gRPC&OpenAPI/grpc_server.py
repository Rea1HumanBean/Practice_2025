from threading import Thread
import grpc
from concurrent import futures
import schedule_pb2
import schedule_pb2_grpc

from src.config.config import schedule_service, TIME_PERIOD_HOURS
from src.utils.services import Services
from src.main import app

GRPC_PORT = 5001


class ScheduleService(schedule_pb2_grpc.ScheduleServiceServicer):
    def AddSchedule(self, request, context):
        try:
            schedule_service.add_schedule_taking_medication(
                user_id=request.user_id,
                name_pills=request.name_pills,
                first_day=request.first_day,
                last_day=request.last_day,
                daily_schedule=list(request.daily_schedule),
            )
            return schedule_pb2.Empty()
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))

    def GetSchedule(self, request, context):
        try:
            result = schedule_service.get_user_schedule(request.user_id, request.schedule_id)

            if result is not None:
                return schedule_pb2.UserReturnScheduleData(
                    name_medication=result.name_medication,
                    first_day=result.first_day,
                    last_day=result.last_day,
                    daily_schedule=result.daily_schedule
                )
            else:
                context.abort(grpc.StatusCode.NOT_FOUND, "Schedule not found")
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))

    def GetNextTakings(self, request, context):
        try:
            next_takings = schedule_service.get_user_next_takings(request.user_id)
            result = Services.check_actual_schedule(next_takings, TIME_PERIOD_HOURS)

            response = schedule_pb2.NextTakingsResponse(
                takings=result
            )
            return response
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    schedule_pb2_grpc.add_ScheduleServiceServicer_to_server(ScheduleService(), server)
    server.add_insecure_port('[::]:5001')
    server.start()
    server.wait_for_termination()

def run_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    schedule_pb2_grpc.add_ScheduleServiceServicer_to_server(ScheduleService(), server)
    server.add_insecure_port(f'[::]:{GRPC_PORT}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    grpc_thread = Thread(target=run_grpc_server, daemon=True)
    grpc_thread.start()

    app.run(port=5000, host='0.0.0.0')