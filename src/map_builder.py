from src.map import MBTAMap
from src.route import Route
from src.stop import Stop
from src.line import Line

def build_map(mbta_api, fetch_stops=True, use_lines=False):
    route_json = mbta_api.routes()
    stops = {}
    lines = {}

    if fetch_stops:
        for route_data in route_json:
            stops[route_data['id']] = [Stop(stop_data) for stop_data in mbta_api.stops(route_data['id'])]
    if use_lines:
        line_ids = set([route_data['relationships']['line']['data']['id'] for route_data in route_json])
        lines = {line_id: Line(mbta_api.line(line_id)) for line_id in line_ids}

    routes = []
    for route_data in route_json:
        route_stops = stops.get(route_data['id'], [])
        route_line = lines.get(route_data['relationships']['line']['data']['id'])
        routes.append(Route(route_data, route_stops, route_line, use_lines))
    return MBTAMap(routes)
