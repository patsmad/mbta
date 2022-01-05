import unittest
from tests.mbta_api_mock import MockMBTAAPI
from src.map_builder import build_map

# Simple tests whether an expected valid response is converted correctly in the Builder
class MBTAAPITest(unittest.TestCase):
    def setUp(self):
        mock_routes_response = [
            {'attributes': {'long_name': 'Test Route Name'}, 'id': 'Test Route ID', 'relationships': {'line': {'data': {'id': 'Test Line ID'}}}}
        ]
        mock_stop_response = {
            'Test Route ID': [
                {'attributes': {'name': 'Test Stop Name'}, 'id': 'Test Stop ID'}
            ]
        }
        mock_line_response = {
            'Test Line ID': {'attributes': {'long_name': 'Test Line Name'}, 'id': 'Test Line ID'}
        }

        self.mock_api = MockMBTAAPI(mock_routes_response, mock_stop_response, mock_line_response)
        self.mock_map = build_map(self.mock_api, fetch_stops=True, use_lines=True)

    def test_api(self):
        routes = self.mock_map.routes
        self.assertEqual(len(routes), 1)
        route = routes[0]
        self.assertEqual(route.name,'Test Route Name')
        self.assertEqual(route.id, 'Test Route ID')

        stops = route.stops
        self.assertEqual(len(stops), 1)
        self.assertEqual(stops[0].name, 'Test Stop Name')
        self.assertEqual(stops[0].id, 'Test Stop ID')

        line = route.line
        self.assertEqual(line.name, 'Test Line Name')
        self.assertEqual(line.id, 'Test Line ID')
