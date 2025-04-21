import unittest

from flask import json

from openapi_server.models.data_of_user_request import DataOfUserRequest  # noqa: E501
from openapi_server.models.return_user_actual_schedule import ReturnUserActualSchedule  # noqa: E501
from openapi_server.models.schedule_get200_response import ScheduleGet200Response  # noqa: E501
from openapi_server.models.schedule_get400_response import ScheduleGet400Response  # noqa: E501
from openapi_server.models.schedule_get404_response import ScheduleGet404Response  # noqa: E501
from openapi_server.models.schedule_get500_response import ScheduleGet500Response  # noqa: E501
from openapi_server.models.schedule_post400_response import SchedulePost400Response  # noqa: E501
from openapi_server.models.user_return_schedule_data import UserReturnScheduleData  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_next_takings_get(self):
        """Test case for next_takings_get

        Получение актуального расписания пользователю (По умолчанию на час вперёд)
        """
        query_string = [('user_id', 56)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/next_takings',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_schedule_get(self):
        """Test case for schedule_get

        Получение конкретного расписания
        """
        query_string = [('user_id', 56),
                        ('schedule_id', 56)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/schedule',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_schedule_post(self):
        """Test case for schedule_post

        Добавление расписания приёма лекарств для пользователя
        """
        data_of_user_request = {"user_id":0,"limitation_days":1,"name_pills":"name_pills","number_iters":1}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/schedule',
            method='POST',
            headers=headers,
            data=json.dumps(data_of_user_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_schedules_get(self):
        """Test case for schedules_get

        Получение всех расписаний приёма лекарств пользователя
        """
        query_string = [('user_id', 56)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/schedules',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
