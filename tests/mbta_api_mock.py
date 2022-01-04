from src.route import Route
from src.stop import Stop

class MockMBTAAPI:
    def __init__(self, mock_routes, mock_stops):
        self.mock_routes = mock_routes
        self.mock_stops = mock_stops

    def routes(self):
        return [Route(route_data) for route_data in self.mock_routes['data']]

    def stops(self, route):
        return [Stop(stop_data) for stop_data in self.mock_stops[route.id]['data']]