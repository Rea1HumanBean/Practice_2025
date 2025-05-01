from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
import uvicorn

from src.services.services import Services
from utils import validate_id
from src.model import DataOfUserRequest, ScheduleDateService, UserReturnScheduleData
from config import TIME_PERIOD_HOURS
from src.db_service import init_db, SessionLocal, MedicationSchedule, PostgreSQLScheduleRepository
from src.logger import setup_logger, get_logger, LoggingMiddleware

repo = PostgreSQLScheduleRepository(SessionLocal)
schedule_service = MedicationSchedule(repo)


app = FastAPI()

setup_logger()
app.add_middleware(LoggingMiddleware)


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.post("/schedule", status_code=201)
async def schedule(user_data: DataOfUserRequest):
    try:
        schedule_data: ScheduleDateService = ScheduleDateService(
            limitation_days=user_data.limitation_days,
            daily_iterations=user_data.number_iters,
        )
    except Exception as e:
        get_logger().error({
            "event": "get_schedules",
            "error": e
        })
        raise HTTPException(status_code=400, detail={"error": "Incorrect type", "details": f"{e}"})
    try:
        await schedule_service.add_schedule_taking_medication(
            user_id=user_data.user_id,
            name_pills=user_data.name_pills,
            first_day=schedule_data.first_day,
            last_day=schedule_data.last_day,
            daily_schedule=schedule_data.daily_schedule,
        )
        return JSONResponse(status_code=201, content={"message": "Schedule created"})
    except Exception as e:
        get_logger().error({
            "event": "schedule",
            "error": e
        })
        raise HTTPException(status_code=500, detail={"error": "Incorrect type", "details": f"{e}"})


@app.get("/schedules", status_code=200)
async def get_schedules(user_id: int = Depends(validate_id("user_id"))):
    try:
        result: int | None = await schedule_service.get_user_all_schedule_id(user_id)
        get_logger().debug({
            "event": "get_schedules",
            "data": result
        })

        if result is not None:
            return JSONResponse(status_code=200, content=result)
        else:
            return JSONResponse(status_code=400, content={"error": "Missing required fields"})
    except Exception as e:
        get_logger().error({
            "event": "get_schedules",
            "error": e
        })
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/schedule", status_code=200)
async def get_schedule(user_id: int = Depends(validate_id("user_id")),
                       schedule_id: int = Depends(validate_id("schedule_id"))
                       ):
    try:
        result: UserReturnScheduleData = await schedule_service.get_user_schedule(
            user_id, schedule_id
        )
        get_logger().debug({
            "event": "next_takings_result",
            "data": result.to_dict()
        })

        if not result:
            raise HTTPException(status_code=404, detail="Schedule not found")

        return JSONResponse(status_code=200, content=result.to_dict())

    except Exception as e:
        get_logger().error({
            "event": "get_schedule",
            "error": e
        })
        raise HTTPException(status_code=500, detail={"error": str(e)})


@app.get("/next_takings", status_code=200)
async def next_takings(user_id: int = Depends(validate_id("user_id"))):
    try:
        result: List[UserReturnScheduleData] | None = await schedule_service.get_user_next_takings(
            user_id
        )

        result: List[str] = Services.check_actual_schedule(result, TIME_PERIOD_HOURS)
        get_logger().debug({
            "event": "next_takings_result",
            "actual_medication": result
        })
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        get_logger().error({
            "event": "next_takings",
            "error": e
        })
        raise HTTPException(status_code=500, detail={"error": str(e)})


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000)
