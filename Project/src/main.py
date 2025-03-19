from flask import Flask, request, jsonify
from dataclasses import asdict
from typing import Any, Dict, List
import logging

from .utils.services import Services
from .utils.data_user_request import DataOfUserRequest
from .utils.schedule_date_service import ScheduleDateService
from .utils.user_return_schedule_data import UserReturnScheduleData
from .config.config import schedule_service, TIME_PERIOD_HOURS


logging.basicConfig(level=logging.DEBUG)



app = Flask(__name__)


def validate_id(number_id: int | str) -> int:
    try:
        valid_number_id = int(number_id)
        if valid_number_id <= 0:
            raise ValueError("id cannot be negative")
        return valid_number_id
    except ValueError:
        raise ValueError("id must be an integer")


@app.route("/schedule", methods=["POST"])
def schedule() -> Any:
    data: Dict[str, Any] = request.get_json()

    try:
        user_data: DataOfUserRequest = DataOfUserRequest(**data)
        schedule_data: ScheduleDateService = ScheduleDateService(
            limitation_days=user_data.limitation_days,
            daily_iterations=user_data.number_iters,
        )
    except Exception as e:
        return jsonify({"error": "Incorrect type", "details": e}), 400

    try:
        schedule_service.add_schedule_taking_medication(
            user_id=user_data.user_id,
            name_pills=user_data.name_pills,
            first_day=schedule_data.first_day,
            last_day=schedule_data.last_day,
            daily_schedule=schedule_data.daily_schedule,
        )
        return jsonify(), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/schedules", methods=["GET"])
def get_schedules():
    user_id: Any = request.args.get("user_id")

    if user_id is None:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        result: int | None = schedule_service.get_user_id_schedule(user_id)
        if result is not None:
            return jsonify(result), 200
        else:
            return jsonify({"error": "Schedules not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/schedule", methods=["GET"])
def get_schedule():
    user_id: Any = request.args.get("user_id")
    schedule_id: Any = request.args.get("schedule_id")

    try:
        valid_user_id = validate_id(user_id)
        valid_schedule_id = validate_id(schedule_id)
    except Exception as e:
        return jsonify({"error": "Incorrect type", "details": e}), 400

    try:
        result: UserReturnScheduleData = schedule_service.get_user_schedule(
            valid_user_id, valid_schedule_id
        )

        if result is not None:
            dict_result = asdict(result)
            return jsonify(dict_result), 200
        else:
            return jsonify({"error": "Schedule not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/next_takings", methods=["GET"])
def next_takings():
    user_id: Any = request.args.get("user_id")

    try:
        valid_user_id: int = validate_id(user_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    try:
        result: List[UserReturnScheduleData] = schedule_service.get_user_next_takings(
            valid_user_id
        )
        logging.info(result)

        result: List[str] = Services.check_actual_schedule(result, TIME_PERIOD_HOURS)
        logging.info(result)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
