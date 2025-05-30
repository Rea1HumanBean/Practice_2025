from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util


class ScheduleGet200Response(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, user_id=None, schedule_id=None, name_pills=None):  # noqa: E501
        """ScheduleGet200Response - a model defined in OpenAPI

        :param user_id: The user_id of this ScheduleGet200Response.  # noqa: E501
        :type user_id: int
        :param schedule_id: The schedule_id of this ScheduleGet200Response.  # noqa: E501
        :type schedule_id: int
        :param name_pills: The name_pills of this ScheduleGet200Response.  # noqa: E501
        :type name_pills: str
        """
        self.openapi_types = {
            'user_id': int,
            'schedule_id': int,
            'name_pills': str
        }

        self.attribute_map = {
            'user_id': 'user_id',
            'schedule_id': 'schedule_id',
            'name_pills': 'name_pills'
        }

        self._user_id = user_id
        self._schedule_id = schedule_id
        self._name_pills = name_pills

    @classmethod
    def from_dict(cls, dikt) -> 'ScheduleGet200Response':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The _schedule_get_200_response of this ScheduleGet200Response.  # noqa: E501
        :rtype: ScheduleGet200Response
        """
        return util.deserialize_model(dikt, cls)

    @property
    def user_id(self) -> int:
        """Gets the user_id of this ScheduleGet200Response.


        :return: The user_id of this ScheduleGet200Response.
        :rtype: int
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: int):
        """Sets the user_id of this ScheduleGet200Response.


        :param user_id: The user_id of this ScheduleGet200Response.
        :type user_id: int
        """

        self._user_id = user_id

    @property
    def schedule_id(self) -> int:
        """Gets the schedule_id of this ScheduleGet200Response.


        :return: The schedule_id of this ScheduleGet200Response.
        :rtype: int
        """
        return self._schedule_id

    @schedule_id.setter
    def schedule_id(self, schedule_id: int):
        """Sets the schedule_id of this ScheduleGet200Response.


        :param schedule_id: The schedule_id of this ScheduleGet200Response.
        :type schedule_id: int
        """

        self._schedule_id = schedule_id

    @property
    def name_pills(self) -> str:
        """Gets the name_pills of this ScheduleGet200Response.


        :return: The name_pills of this ScheduleGet200Response.
        :rtype: str
        """
        return self._name_pills

    @name_pills.setter
    def name_pills(self, name_pills: str):
        """Sets the name_pills of this ScheduleGet200Response.


        :param name_pills: The name_pills of this ScheduleGet200Response.
        :type name_pills: str
        """

        self._name_pills = name_pills
