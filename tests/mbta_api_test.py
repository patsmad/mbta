import unittest
from tests.mbta_api_mock import MockMBTAAPI

# Simple tests whether an expected valid response is converted correctly in the API
class MBTAAPITest(unittest.TestCase):
    def setUp(self):
        mock_routes_response = {
            'data': [
                {'attributes': {'long_name': 'Test Route Name'}, 'id': 'Test Route ID'}
            ]
        }
        mock_stop_response = {
            'Test Route ID': {
                'data': [
                    {'attributes': {'name': 'Test Stop Name'}, 'id': 'Test Stop ID'}
                ]
            }
        }

        self.mock_api = MockMBTAAPI(mock_routes_response, mock_stop_response)

    def test_api(self):
        routes = self.mock_api.routes()
        self.assertEqual(len(routes), 1)
        self.assertEqual(routes[0].name,'Test Route Name')
        self.assertEqual(routes[0].id, 'Test Route ID')

        stops = self.mock_api.stops(routes[0])
        self.assertEqual(len(stops), 1)
        self.assertEqual(stops[0].name, 'Test Stop Name')
        self.assertEqual(stops[0].id, 'Test Stop ID')
