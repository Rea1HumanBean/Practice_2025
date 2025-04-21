import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.data_of_user_request import DataOfUserRequest  # noqa: E501
from openapi_server.models.return_user_actual_schedule import ReturnUserActualSchedule  # noqa: E501
from openapi_server.models.schedule_get200_response import ScheduleGet200Response  # noqa: E501
from openapi_server.models.schedule_get400_response import ScheduleGet400Response  # noqa: E501
from openapi_server.models.schedule_get404_response import ScheduleGet404Response  # noqa: E501
from openapi_server.models.schedule_get500_response import ScheduleGet500Response  # noqa: E501
from openapi_server.models.schedule_post400_response import SchedulePost400Response  # noqa: E501
from openapi_server.models.user_return_schedule_data import UserReturnScheduleData  # noqa: E501
from openapi_server import util


def next_takings_get(user_id):  # noqa: E501
    """Получение актуального расписания пользователю (По умолчанию на час вперёд)

    Получение актуального расписания по user_id # noqa: E501

    :param user_id: ID пользователя
    :type user_id: int

    :rtype: Union[List[ReturnUserActualSchedule], Tuple[List[ReturnUserActualSchedule], int], Tuple[List[ReturnUserActualSchedule], int, Dict[str, str]]
    """
    return 'do some magic!'


def schedule_get(user_id, schedule_id):  # noqa: E501
    """Получение конкретного расписания

    Возвращает расписание по user_id и schedule_id # noqa: E501

    :param user_id: ID пользователя
    :type user_id: int
    :param schedule_id: ID расписания
    :type schedule_id: int

    :rtype: Union[ScheduleGet200Response, Tuple[ScheduleGet200Response, int], Tuple[ScheduleGet200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def schedule_post(body):  # noqa: E501
    """Добавление расписания приёма лекарств для пользователя

    Создает новое расписание приема лекарств для указанного пользователя # noqa: E501

    :param data_of_user_request: 
    :type data_of_user_request: dict | bytes

    :rtype: Union[object, Tuple[object, int], Tuple[object, int, Dict[str, str]]
    """
    data_of_user_request = body
    if connexion.request.is_json:
        data_of_user_request = DataOfUserRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def schedules_get(user_id):  # noqa: E501
    """Получение всех расписаний приёма лекарств пользователя

    Возвращает все расписания пользователя # noqa: E501

    :param user_id: ID пользователя
    :type user_id: int

    :rtype: Union[List[UserReturnScheduleData], Tuple[List[UserReturnScheduleData], int], Tuple[List[UserReturnScheduleData], int, Dict[str, str]]
    """
    return 'do some magic!'
