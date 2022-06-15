import unittest
from unittest.mock import Mock, patch
from unittest import skipIf

from nose.tools import assert_is_not_none, assert_equal,assert_list_equal

from project.services import get_users_data
from project.constants import SKIP_REAL


class TestUsersAPI(unittest.TestCase):
    @patch('project.services.requests.get')
    def test_getting_users_data(self,mock_get):
        # Configure the mock to return a response with an OK status code.
        mock_get.return_value.ok = True

        # Call the service, which will send a request to the server.
        response = get_users_data()

        # If the request is sent successfully, then I expect a response to be returned.
        assert_is_not_none(response)
        
        
    @patch('project.services.requests.get')
    def test_getting_users_data_when_response_is_ok(self,mock_get):
        users_data = {'01-01-2022': 300}
        # Configure the mock to return a response with an OK status code. Also, the mock should have           
        # a `json()` method that returns a users_data.
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = users_data
        # Call the service, which will send a request to the server.
        response = get_users_data()
        # If the request is sent successfully, then I expect a response to be returned.
        assert_equal(response.json(), users_data)

        
    @skipIf(SKIP_REAL, 'Skipping tests that hit the real API server.')
    def test_integration_contract(self):
        # Call the service to hit the actual API.
        actual = get_users_data()
        actual_keys = list(actual.json().keys()).pop()
        # Call the service to hit the mocked API.
        with patch('project.services.requests.get') as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = {
                "01-01-2022":300,"02-01-2022":500,"03-01-2022":700,
                "04-01-2022":1300,"05-01-2022":2000,"06-01-2022":3000,
                "07-01-2022":3500,"08-01-2022":4000,"09-01-2022":4500,
                "10-01-2022":5000,"11-01-2022":20000,"12-01-2022":35000,
                "13-01-2022":46000,"14-01-2022":70000,"15-01-2022":90000
                }
            mocked = get_users_data()
            mocked_keys = list(mocked.json().keys()).pop()
        # An object from the actual API and an object from the mocked API should have
        # the same data structure.
        assert_list_equal(list(actual_keys), list(mocked_keys))