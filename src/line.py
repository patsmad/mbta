class Line:
    def __init__(self, line_json):
        self.id = line_json['id']
        self.name = line_json['attributes']['long_name']
