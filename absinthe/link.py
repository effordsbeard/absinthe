from furl import furl

class Link(object):

    def __init__(self):
        self.f = None

    def from_url(self, url):
        self.f = furl(url)

    def join(self, paths=[]):
        if not isinstance(paths, list):
            paths = [paths]
        for path in paths:
            self.f.join(path)

    def url(self):
        return self.f.url

    def test(self):
        pass
