from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util


class ScheduleGet500Response(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, error=None):  # noqa: E501
        """ScheduleGet500Response - a model defined in OpenAPI

        :param error: The error of this ScheduleGet500Response.  # noqa: E501
        :type error: str
        """
        self.openapi_types = {
            'error': str
        }

        self.attribute_map = {
            'error': 'error'
        }

        self._error = error

    @classmethod
    def from_dict(cls, dikt) -> 'ScheduleGet500Response':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The _schedule_get_500_response of this ScheduleGet500Response.  # noqa: E501
        :rtype: ScheduleGet500Response
        """
        return util.deserialize_model(dikt, cls)

    @property
    def error(self) -> str:
        """Gets the error of this ScheduleGet500Response.


        :return: The error of this ScheduleGet500Response.
        :rtype: str
        """
        return self._error

    @error.setter
    def error(self, error: str):
        """Sets the error of this ScheduleGet500Response.


        :param error: The error of this ScheduleGet500Response.
        :type error: str
        """

        self._error = error
