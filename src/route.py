class Route:
    def __init__(self, route_json):
        self.attributes = route_json['attributes']
        self.id = route_json['id']
        self.name = self.attributes['long_name']
