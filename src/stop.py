class Stop:
    def __init__(self, stop_json):
        self.attributes = stop_json['attributes']
        self.name = self.attributes['name']
        self.id = stop_json['id']
