from .asset import Asset
from .image import Image
import re
import os, os.path


class Style(Asset):

    def __init__(self, base, ref='', *args, **kwargs):
        super().__init__(base, ref, *args, **kwargs)
        if self.src_name:
            if not '.' in self.src_name:
                self.src_name += '.css'
        self.name += '.css'
        self.file_type = 'text'

    def parse_assets(self):
        if not self.text:
            return

        base = self.getpath()

        for import_url in self.imports():
            asset = Style(base, import_url)
            if self.handle_asset(asset, subfolder='style'):
                self.text = self.text.replace(import_url, os.path.relpath(asset.saved_path, self.saved_path).replace('../', './', 1))
                self.save()

        for url in self.urls():
            cls = Image
            subfolder = 'image'
            if '.' in url:
                try:
                    ext = url.split('.')[-1]
                except Exception as e:
                    ext = ''
                if ext in ['ttf', 'woff', 'woff2', 'otf', 'eot']:
                    cls = Asset
                    subfolder = 'font'
            asset = cls(base, url)
            if self.handle_asset(asset, subfolder=subfolder):
                self.text = self.text.replace(url, os.path.relpath(asset.saved_path, self.saved_path).replace('../', './', 1))
                self.save()

        super().parse_assets()

    def handle_asset(self, asset, subfolder=''):
        if self.main_set.get(asset.getpath()):
            return False

        self.main_set.add(asset)

        asset.main_set = self.main_set
        asset.dist = self.dist
        if not asset.saved_path:
            asset.load()
            asset.save(subfolder=subfolder)

        return True

    def imports(self):
        res = []
        for match in re.findall(r'@import[^;]+;', self.text):
            res.append(match.replace(' ', '').replace('@import', '').replace('url(', '').replace(')', '').replace(';', '').replace('""', '').replace('\'', ''))
        return res

    def urls(self):
        res = []
        for match in re.findall(r'url\([^)]+\)', self.text):
            res.append(match.replace(' ', '').replace('url(', '').replace(')', '').replace(';', '').replace('"', '').replace('\'', ''))
        return res
