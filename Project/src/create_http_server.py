from fastapi import FastAPI


from src.logger import setup_logger, LoggingMiddleware
from src.transports import schedule_router, schedules_router, next_takings_router
from src.db_service.db import init_db


def create_http_server() -> FastAPI:
    app = FastAPI()

    setup_logger()
    app.add_middleware(LoggingMiddleware)

    app.include_router(schedule_router)
    app.include_router(schedules_router)
    app.include_router(next_takings_router)

    @app.on_event("startup")
    async def startup_event():
        await init_db()

    return app
