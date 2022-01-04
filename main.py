from src.mbta_api import MBTAAPI
from src.map_builder import build_map
import subprocess
import json

def get_api_key():
    with open('config.json', 'r') as f:
        data = json.load(f)
    return data['api-key']

def run():
    api = MBTAAPI(get_api_key())
    mbta_map = build_map(api)
    route_names = mbta_map.get_all_route_names()
    print(', '.join(route_names))
    max_id, max_stops = mbta_map.get_max_route()
    min_id, min_stops = mbta_map.get_min_route()
    print("Route with max stops: {} ({})".format(max_id, len(max_stops)))
    print("Route with min stops: {} ({})".format(min_id, len(min_stops)))
    print("All stops with multiple routes:")
    for connecting_stop in mbta_map.connecting_stops:
        print("\t{} - Routes: {}".format(connecting_stop, ', '.join(mbta_map.stops_to_routes[connecting_stop])))

    stop1 = "Davis"
    stop2 = "Kendall/MIT"
    path = mbta_map.find_connecting_path(stop1, stop2)
    if len(path) == 0:
        print('Invalid stop(s). Check spelling and make sure the stops are currently connected to the network')
    else:
        print("{} to {}: {}".format(stop1, stop2, ', '.join(path)))

def run_tests():
    subprocess.run("python -m unittest tests.map_test tests.mbta_api_test -v")

# TODO: Add in command line stuff
if __name__ == '__main__':
    run()