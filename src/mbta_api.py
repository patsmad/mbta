import requests

class MBTAAPI:
    core_url = 'https://api-v3.mbta.com'
    routes_url = 'routes'
    stops_url = 'stops'
    line_url = 'lines'

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
        return self.get_response("{}/{}?filter[type]=0,1&include=line".format(self.core_url, self.routes_url))['data']

    def stops(self, route_id):
        return self.get_response("{}/{}?filter[route]={}".format(self.core_url, self.stops_url, route_id))['data']

    def line(self, line_id):
        return self.get_response("{}/{}/{}".format(self.core_url, self.line_url, line_id))['data']
