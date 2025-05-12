from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from src.config import TIME_PERIOD_HOURS
from src.db_service import MedicationSchedule
from src.logger import get_logger
from src.model import UserReturnScheduleData
from src.services import validate_id, Services
from src.utils import RepositoryProvider

next_takings_router = APIRouter(prefix="/next_takings")


@next_takings_router.get("", status_code=status.HTTP_200_OK)
async def next_takings(
    user_id: Annotated[int, Depends(validate_id("user_id"))],
    schedule_service: Annotated[
        MedicationSchedule, Depends(RepositoryProvider.get_instance)
    ],
) -> JSONResponse:
    try:
        medications: list[UserReturnScheduleData] | None = (
            await schedule_service.get_user_next_takings(user_id)
        )
        upcoming_meds: list[str] | None = Services.actual_schedule(
            medications, TIME_PERIOD_HOURS
        )

        get_logger().debug(
            {"event": "next_takings_result", "actual_medication": upcoming_meds}
        )
        return JSONResponse(status_code=200, content=upcoming_meds)
    except ValueError as e:
        get_logger().error({"event": "id_validation", "error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Invalid request data", "details": str(e)},
        )

    except Exception as e:
        get_logger().error({"event": "get_schedules", "error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": str(e)}
        )
