import unittest
from tests.mbta_api_mock import MockMBTAAPI
from src.map_builder import build_map

class MapTest(unittest.TestCase):
    def getRoute(self, letter):
        return {'attributes': {'long_name': 'Route {}'.format(letter)}, 'id': 'Route {} ID'.format(letter)}

    def getStop(self, letter):
        return {'attributes': {'name': 'Stop {}'.format(letter)}, 'id': 'Stop {} ID'.format(letter)}

    def setUp(self):
        routes = {letter: self.getRoute(letter) for letter in ['A', 'B', 'C']}
        stops = {letter: self.getStop(letter) for letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G']}
        mock_routes_response = {
            'data': list(routes.values())
        }
        mock_stop_response = {
            'Route A ID': {
                'data': [stops[letter] for letter in ['A', 'B', 'C', 'D']]
            },
            'Route B ID': {
                'data': [stops[letter] for letter in ['E', 'B', 'F']]
            },
            'Route C ID': {
                'data': [stops[letter] for letter in ['G']]
            }
        }
        self.mock_map = build_map(MockMBTAAPI(mock_routes_response, mock_stop_response))
        self.empty_map = build_map(MockMBTAAPI({'data': []}, {'data': []}))

    def test_route_names(self):
        route_names = self.mock_map.get_all_route_names()
        self.assertEqual(len(route_names), 3)
        self.assertIn('Route A', route_names)
        self.assertIn('Route B', route_names)
        self.assertIn('Route C', route_names)

    def test_empty_route_names(self):
        route_names = self.empty_map.get_all_route_names()
        self.assertEqual(len(route_names), 0)

    def test_min_value(self):
        route_id, stops = self.mock_map.get_min_route()
        self.assertEqual(route_id, 'Route C ID')
        self.assertEqual(len(stops), 1)

    def test_empty_min(self):
        route_id, stops = self.empty_map.get_min_route()
        self.assertIsNone(route_id)
        self.assertEqual(len(stops), 0)

    def test_max_value(self):
        route_id, stops = self.mock_map.get_max_route()
        self.assertEqual(route_id, 'Route A ID')
        self.assertEqual(len(stops), 4)

    def test_empty_max(self):
        route_id, stops = self.empty_map.get_max_route()
        self.assertIsNone(route_id)
        self.assertEqual(len(stops), 0)

    def test_connecting_routes(self):
        stop_to_routes = self.mock_map.connecting_stops
        self.assertEqual(len(stop_to_routes), 1)
        self.assertIn('Stop B', stop_to_routes)
        self.assertEqual(len(self.mock_map.stops_to_routes['Stop B']), 2)
        self.assertIn('Route A ID', self.mock_map.stops_to_routes['Stop B'])
        self.assertIn('Route B ID', self.mock_map.stops_to_routes['Stop B'])

    def test_same_station_path(self):
        same_station_path = self.mock_map.find_connecting_path('Stop A', 'Stop A')
        self.assertEqual(len(same_station_path), 1)
        self.assertEqual(same_station_path[0], 'Route A ID')

    def test_same_route_path(self):
        same_route_path = self.mock_map.find_connecting_path('Stop A', 'Stop C')
        self.assertEqual(len(same_route_path), 1)
        self.assertEqual(same_route_path[0], 'Route A ID')

    def test_different_route_path(self):
        different_route_path = self.mock_map.find_connecting_path('Stop A', 'Stop E')
        self.assertEqual(len(different_route_path), 2)
        self.assertIn('Route A ID', different_route_path)
        self.assertIn('Route B ID', different_route_path)

    def test_crossing_route_path(self):
        crossing_route_path = self.mock_map.find_connecting_path('Stop B', 'Stop E')
        self.assertEqual(len(crossing_route_path), 1)
        self.assertEqual(crossing_route_path[0], 'Route B ID')

    def test_isolated_route_path(self):
        isolated_stop_path = self.mock_map.find_connecting_path('Stop A', 'Stop G')
        self.assertEqual(len(isolated_stop_path), 0)

    def test_empty_path(self):
        no_stops = self.empty_map.find_connecting_path('Stop A', 'Stop B')
        self.assertEqual(len(no_stops), 0)
