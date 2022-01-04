from src.map import MBTAMap

def build_map(mbta_api):
    routes = mbta_api.routes()
    stops = {route.id: mbta_api.stops(route) for route in routes}
    return MBTAMap(routes, stops)
