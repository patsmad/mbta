class Route:
    def __init__(self, route_data, route_stops, route_line, use_lines):
        self.id = route_data['id']
        self.name = route_data['attributes']['long_name']
        self.line = route_line
        self.stops = route_stops
        self.group = self.name if not use_lines else self.line.name
