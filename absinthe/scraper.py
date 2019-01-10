from .page import Page
from .assetset import AssetSet


class Scraper(object):

    def __init__(self, config={}):
        self.config = config
        self.assets = AssetSet()

    def run(self):
        self.index = Page(self.config.get('source'),
                            self.config.get('index'),
                            # should_load=self.should_load,
                            # ignore_query=False, \
                            check_url=self.check_url,
                            check_text=self.check_text,
                            name=self.config.get('dist_index', 'index.html'),
                            main_set=self.assets,
                            max_depth=self.config.get('depth'),
                            asset_selectors=self.config.get('assets'),
                            dist=self.config.get('dist'))

        self.index.load()

        self.index.save(name=self.config.get('dist_index', 'index.html'))
        self.index.parse_assets()
        self.index.save()


    def check_url(self, url):
        if not url:
            return True
        skip = self.config.get('skip').get('url', {}).get('contains', [])
        for part in skip:
            if part in url:
                return False
        return True

    def check_text(self, text):
        if not text:
            return True
        skip = self.config.get('skip').get('text', {}).get('contains', [])
        for part in skip:
            if part in text:
                return False
        return True

    def should_load(self, asset):
        if self.assets.has(asset):
            return False
        # TODO: более комплексные фильтры на случай повторяемых ссылок
        return True
