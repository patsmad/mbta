class MBTAMap:
    def __init__(self, routes):
        self.routes = routes
        self.sorted_routes = sorted(self.routes, key=lambda x: len(x.stops))
        self.stops_to_routes = self.get_stops_to_route()
        self.connecting_stops = [stop_name for stop_name, routes in self.stops_to_routes.items() if len(routes) > 1]
        self.route_connections = self.get_route_connections()

    def get_stops_to_route(self):
        stops_to_routes = {}
        for route in self.routes:
            for stop in route.stops:
                if stop.name not in stops_to_routes:
                    stops_to_routes[stop.name] = []
                if route.group not in stops_to_routes[stop.name]:
                    stops_to_routes[stop.name].append(route.group)
        return stops_to_routes

    def get_route_connections(self):
        route_connections = {route.group: [] for route in self.routes}
        for connecting_stop in self.connecting_stops:
            for route_idx, route1 in enumerate(self.stops_to_routes[connecting_stop]):
                for route2 in self.stops_to_routes[connecting_stop][route_idx + 1:]:
                    route_connections[route1].append(route2)
                    route_connections[route2].append(route1)
        return route_connections

    def get_all_route_names(self):
        return [route.name for route in self.routes]

    def get_route_by_sorted_index(self, idx):
        if len(self.sorted_routes) == 0:
            return None, []
        return self.sorted_routes[idx].id, self.sorted_routes[idx].stops

    def get_min_route(self):
        return self.get_route_by_sorted_index(0)

    def get_max_route(self):
        return self.get_route_by_sorted_index(-1)

    def find_connecting_path(self, stop1, stop2):
        missing_stops = [stop for stop in [stop1, stop2] if stop not in self.stops_to_routes]
        path = []
        if len(missing_stops) == 0:
            path = self.breadth_first_search(stop1, stop2)
        return path

    def breadth_first_search(self, stop1, stop2):
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
