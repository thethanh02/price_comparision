# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestProductController(BaseTestCase):
    """ProductController integration test stubs"""

    def test_api_product_get(self):
        """Test case for api_product_get

        
        """
        query_string = [('name', 'name_example')]
        response = self.client.open(
            '/api/product',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_stream_get(self):
        """Test case for stream_get

        
        """
        response = self.client.open(
            '/stream',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
