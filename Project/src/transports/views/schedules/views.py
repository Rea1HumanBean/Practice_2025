from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from src.db_service import MedicationSchedule
from src.logger import get_logger
from src.services import validate_id
from src.utils import RepositoryProvider

schedules_router = APIRouter(prefix="/schedules")


@schedules_router.get("", status_code=status.HTTP_200_OK)
async def get_schedules(
    user_id: Annotated[int, Depends(validate_id("user_id"))],
    schedule_service: Annotated[
        MedicationSchedule, Depends(RepositoryProvider.get_instance)
    ],
) -> JSONResponse:
    try:
        user_schedule_id: list[int] | None = (
            await schedule_service.get_user_all_schedule_id(user_id)
        )
        get_logger().debug({"event": "get_schedules", "data": user_schedule_id})

        if user_schedule_id is not None:
            return JSONResponse(status_code=200, content=user_schedule_id)
        else:
            return JSONResponse(
                status_code=400, content={"error": "Missing required fields"}
            )
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
