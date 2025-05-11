class Url(object):
    short_url = None
    actual_url = None
    timestamp = None
    def __init__(self, short_url, actual_url, timestamp):
        self.short_url = short_url
        self.actual_url = actual_url
        self.timestamp = timestamp

def make_url(short_url, actual_url, timestamp):
    url = Url(short_url, actual_url, timestamp)
    return url