# coding: utf-8

"""
    Schedule OpenApi

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from openapi_client.models.schedule_get404_response import ScheduleGet404Response

class TestScheduleGet404Response(unittest.TestCase):
    """ScheduleGet404Response unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ScheduleGet404Response:
        """Test ScheduleGet404Response
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ScheduleGet404Response`
        """
        model = ScheduleGet404Response()
        if include_optional:
            return ScheduleGet404Response(
                error = ''
            )
        else:
            return ScheduleGet404Response(
        )
        """

    def testScheduleGet404Response(self):
        """Test ScheduleGet404Response"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
