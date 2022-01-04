from src.mbta_api import MBTAAPI
from src.map_builder import build_map
import subprocess
import json
import sys

class Arguments:
    def __init__(self, arg_array):
        self.run_get_route_names = '--print_routes' in arg_array
        self.run_get_min_stops = '--print_min_stops' in arg_array or '--print_stop_analysis' in arg_array
        self.run_get_max_stops = '--print_max_stops' in arg_array or '--print_stop_analysis' in arg_array
        self.run_get_connecting_stops = '--print_connecting_stops' in arg_array or '--print_stop_analysis' in arg_array

        path_arg = [arg for arg in arg_array if '--get_path=' in arg]
        self.run_path = len(path_arg) > 0
        paths = path_arg[0].split('--get_path=')[1].split(',') if self.run_path else []
        self.path1 = paths[0] if len(paths) > 0 else ""
        self.path2 = paths[1] if len(paths) > 1 else ""

        self.run_tests = '--run_tests' in arg_array

        self.api_arg = [arg for arg in arg_array if '--api_key=' in arg]
        self.api_key = self.api_arg[0].split('--api_key=')[1] if len(self.api_arg) > 0 else None

        self.use_lines = '--use_lines' in arg_array

    def need_map(self):
        return self.run_get_route_names or self.run_get_min_stops or self.run_get_max_stops or self.run_get_connecting_stops or self.run_path

    def fetch_stops(self):
        return self.run_get_min_stops or self.run_get_max_stops or self.run_get_connecting_stops or self.run_path

    def fetch_lines(self):
        return self.use_lines and self.run_path

def get_api_key():
    try:
        with open('config.json', 'r') as f:
            data = json.load(f)
        return data['api-key']
    except:
        print("Warning: You have not set an api key and a config file doesn't exist. Your API requests may be throttled")

def run_tests():
    subprocess.run("python -m unittest tests.map_test tests.mbta_api_test -v")

def run(arguments):
    if arguments.run_tests:
        print("Running tests (note, other operations won't run when --run_tests is set)")
        run_tests()
    elif arguments.need_map():
        api_key = arguments.api_key if arguments.api_key is not None else get_api_key()
        api = MBTAAPI(api_key)
        mbta_map = build_map(api, arguments.fetch_stops(), arguments.fetch_lines())

        if arguments.run_get_route_names:
            route_names = mbta_map.get_all_route_names()
            print('Routes: {}'.format(', '.join(route_names)))
        if arguments.run_get_max_stops:
            max_id, max_stops = mbta_map.get_max_route()
            print("Route with max stops: {} ({})".format(max_id, len(max_stops)))
        if arguments.run_get_min_stops:
            min_id, min_stops = mbta_map.get_min_route()
            print("Route with min stops: {} ({})".format(min_id, len(min_stops)))
        if arguments.run_get_connecting_stops:
            print("All stops with multiple routes:")
            for connecting_stop in mbta_map.connecting_stops:
                print("\t{} - Routes: {}".format(connecting_stop, ', '.join(mbta_map.stops_to_routes[connecting_stop])))
        if arguments.run_path:
            path = mbta_map.find_connecting_path(arguments.path1, arguments.path2)
            if len(path) == 0:
                print('Invalid stop(s). Check spelling and make sure the stops are currently connected to the network')
            else:
                print("{} to {}: {}".format(arguments.path1, arguments.path2, ', '.join(path)))

if __name__ == '__main__':
    run(Arguments(sys.argv[1:]))