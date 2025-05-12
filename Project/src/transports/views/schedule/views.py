from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from src.db_service import MedicationSchedule
from src.logger import get_logger
from src.model import DataOfUserRequest, ScheduleDateService, UserReturnScheduleData
from src.services import validate_id
from src.utils import RepositoryProvider

schedule_router = APIRouter(prefix="/schedule")


@schedule_router.post("", status_code=status.HTTP_201_CREATED)
async def create_user_schedule(
    user_data: DataOfUserRequest,
    schedule_service: Annotated[
        MedicationSchedule, Depends(RepositoryProvider.get_instance)
    ],
) -> JSONResponse:
    try:
        schedule_data = ScheduleDateService(
            limitation_days=user_data.limitation_days,
            daily_iterations=user_data.number_iters,
        )

        await schedule_service.add_schedule_taking_medication(
            user_id=user_data.user_id,
            name_pills=user_data.name_pills,
            first_day=schedule_data.first_day,
            last_day=schedule_data.last_day,
            daily_schedule=schedule_data.daily_schedule,
        )

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Schedule created successfully"},
        )

    except ValueError as e:
        get_logger().error({"event": "data_validation", "error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Invalid request data", "details": str(e)},
        )

    except Exception as e:
        get_logger().error({"event": "schedule_creation", "error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Schedule creation failed"},
        )


@schedule_router.get("", status_code=status.HTTP_200_OK)
async def get_user_schedule(
    user_id: Annotated[int, Depends(validate_id("user_id"))],
    schedule_id: Annotated[int, Depends(validate_id("schedule_id"))],
    schedule_service: Annotated[
        MedicationSchedule, Depends(RepositoryProvider.get_instance)
    ],
) -> JSONResponse:
    try:
        result_users_schedules: UserReturnScheduleData | None = (
            await schedule_service.get_user_schedule(user_id, schedule_id)
        )

        get_logger().debug(
            {"event": "next_takings_result", "data": result_users_schedules}
        )

        if not result_users_schedules:
            raise HTTPException(status_code=404, detail="Schedule not found")

        return JSONResponse(status_code=200, content=result_users_schedules.to_dict())

    except ValueError as e:
        get_logger().error({"event": "id_validation", "error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Invalid request data", "details": str(e)},
        )

    except Exception as e:
        get_logger().error({"event": "get_user_schedule", "error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Haven't schedule for this user", "details": str(e)},
        )
