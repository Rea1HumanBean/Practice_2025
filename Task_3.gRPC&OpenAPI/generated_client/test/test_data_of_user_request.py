# coding: utf-8

"""
    Schedule OpenApi

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from openapi_client.models.data_of_user_request import DataOfUserRequest

class TestDataOfUserRequest(unittest.TestCase):
    """DataOfUserRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DataOfUserRequest:
        """Test DataOfUserRequest
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DataOfUserRequest`
        """
        model = DataOfUserRequest()
        if include_optional:
            return DataOfUserRequest(
                user_id = 56,
                name_pills = '',
                limitation_days = 1,
                number_iters = 56
            )
        else:
            return DataOfUserRequest(
                user_id = 56,
                name_pills = '',
                limitation_days = 1,
                number_iters = 56,
        )
        """

    def testDataOfUserRequest(self):
        """Test DataOfUserRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
