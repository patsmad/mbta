class MockMBTAAPI:
    def __init__(self, mock_routes, mock_stops, mock_lines):
        self.mock_routes = mock_routes
        self.mock_stops = mock_stops
        self.mock_lines = mock_lines

    def routes(self):
        return self.mock_routes

    def stops(self, route_id):
        return self.mock_stops[route_id]

    def line(self, line_id):
        return self.mock_lines[line_id]