import asyncio

import grpc

from gRPC import schedule_pb2_grpc
from gRPC.schedule_grpc_service import ScheduleService
from gRPC.utils.dependency import Dependency
from src.logger import get_logger


async def create_grpc_server():
    deps = Dependency()
    await deps.initialize()

    service = ScheduleService(deps.schedule_service)

    server = grpc.aio.server()
    schedule_pb2_grpc.add_ScheduleServiceServicer_to_server(service, server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    get_logger().info("Server Started")

    try:
        await server.wait_for_termination()
    except asyncio.CancelledError:
        get_logger().info("Server shutting down...")
        await server.stop(0)


async def run_grpc_server():
    try:
        await create_grpc_server()
    except KeyboardInterrupt:
        get_logger().info("Interrupted by user")
