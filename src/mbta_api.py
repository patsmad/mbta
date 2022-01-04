import requests
from src.route import Route
from src.stop import Stop

class MBTAAPI:
    core_url = 'https://api-v3.mbta.com'
    routes_url = 'routes'
    stops_url = 'stops'

    def __init__(self, api_key):
        self.headers = {}
        if api_key:
            self.headers['x-api-key'] = api_key

    def get_response(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception("Request Error Code {} for {}".format(response.status_code, url))
        else:
            return response.json()

    def routes(self):
        route_json = self.get_response("{}/{}?filter[type]=0,1".format(self.core_url, self.routes_url))
        return [Route(route_data) for route_data in route_json['data']]

    def stops(self, route):
        stop_json = self.get_response("{}/{}?filter[route]={}".format(self.core_url, self.stops_url, route.id))
        return [Stop(stop_data) for stop_data in stop_json['data']]
