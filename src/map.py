class MBTAMap:
    def __init__(self, routes, routes_to_stops):
        self.routes = routes
        self.routes_to_stops = routes_to_stops
        self.sorted_routes_ids = sorted(self.routes_to_stops, key=lambda x: len(self.routes_to_stops[x]))
        self.stops_to_routes = {}
        for route_id, stops in self.routes_to_stops.items():
            for stop in stops:
                if stop.name not in self.stops_to_routes:
                    self.stops_to_routes[stop.name] = []
                self.stops_to_routes[stop.name].append(route_id)
        self.connecting_stops = [stop_name for stop_name, routes in self.stops_to_routes.items() if len(routes) > 1]
        self.route_connections = {route_id: [] for route_id in self.routes_to_stops}
        for connecting_stop in self.connecting_stops:
            for route_idx, route1 in enumerate(self.stops_to_routes[connecting_stop]):
                for route2 in self.stops_to_routes[connecting_stop][route_idx + 1:]:
                    self.route_connections[route1].append(route2)
                    self.route_connections[route2].append(route1)


    def get_all_route_names(self):
        return [route.name for route in self.routes]

    def get_route_by_sorted_index(self, idx):
        if len(self.sorted_routes_ids) == 0:
            return None, []
        return self.sorted_routes_ids[idx], self.routes_to_stops[self.sorted_routes_ids[idx]]

    def get_min_route(self):
        return self.get_route_by_sorted_index(0)

    def get_max_route(self):
        return self.get_route_by_sorted_index(-1)

    def find_connecting_path(self, stop1, stop2):
        missing_stops = [stop for stop in [stop1, stop2] if stop not in self.stops_to_routes]
        path = []
        if len(missing_stops) == 0:
            path = self.depth_first_search(stop1, stop2)
        return path

    def depth_first_search(self, stop1, stop2):
        parents = {route_id: None for route_id in self.stops_to_routes[stop1]}
        queue = [route_id for route_id in self.stops_to_routes[stop1]]
        destination_routes = self.stops_to_routes[stop2]
        while len(queue) > 0:
            route_id = queue.pop(0)
            if route_id in destination_routes:
                return self.rewind_path(parents, route_id)

            for connecting_route_id in self.route_connections[route_id]:
                if connecting_route_id not in parents:
                    parents[connecting_route_id] = route_id
                    queue.append(connecting_route_id)
        return []

    def rewind_path(self, parents, route_id):
        path = [route_id]
        while parents[route_id]:
            route_id = parents[route_id]
            path.append(route_id)
        return path[::-1]
