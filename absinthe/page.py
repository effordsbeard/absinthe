from .asset import Asset
from .style import Style
from .script import Script
from .image import Image
import uuid
from pyquery import PyQuery as pq
from termcolor import colored
import os, os.path

asset_selectors = {
    'a/href': 'page',
    'iframe/src': 'page',
    'img/src': 'image',
    'video/src': 'media',
    'source/src': 'media',
    'audio/src': 'media',
    'link[rel=stylesheet]/href': 'style',
    'style/': 'style',
    'script/src': 'script',
    'link:not([rel=stylesheet])/href': 'other'
}

class Page(Asset):

    def __init__(self, base, ref='', main_set=None, root_selector=None, depth=0, max_depth=0, asset_selectors=asset_selectors, name='index.html', *args, **kwargs):
        super().__init__(base, ref, *args, **kwargs)
        self.root_selector = root_selector
        self.depth = depth
        self.max_depth = max_depth
        self.main_set = main_set
        self.asset_selectors = asset_selectors
        self.pages = []
        self.src_name = name
        self.name = self.name + '.html'
        self.file_type = 'text'

    def pq(self):
        self.d = pq(self.text)

        if self.root_selector:
            self.d('body').html(self.d(self.root_selector).outerHtml())

    def parse_assets(self):
        if not hasattr(self, 'd'):
            self.pq()

        base = self.d('base')
        if not base:
            base = self.getpath()
        else:
            base = pq(base).attr('href')

        for asset_selector, _type in self.asset_selectors.items():
            type = _type
            subfolder = _type
            if not isinstance(_type, str):
                type = _type.get('type')
                subfolder = _type.get('folder')
            try:
                selector, attribute = asset_selector.split('/')
            except:
                print(colored('Error: incorrect asset selector - ', 'red', attrs=['bold']), colored(asset_selector, attrs=['bold']))
                continue

            for elem in self.d(selector):
                if attribute:
                    ref = pq(elem).attr(attribute)
                else:
                    ref = None
                if not self.check_url(ref):
                    continue
                ref = ref if ref else None
                asset = None
                has_text = False
                if pq(elem).text():
                    if not self.check_text(pq(elem).text()):
                        continue

                if type == 'page':
                    if ref.startswith('#'):
                        continue
                    asset = Page(base, ref, name=ref.split('/')[-1] or ref, depth=self.depth + 1, max_depth=self.max_depth, asset_selectors=asset_selectors)

                elif type == 'image':
                    asset = Image(base, ref)

                elif type == 'style':
                    asset = Style(base, ref, text=pq(elem).text())
                    if pq(elem).text():
                        has_text = True
                        id = uuid.uuid4().hex
                        new_elem = pq('<link id="%s" rel="stylesheet" href="%s" />' % (id, pq(elem).attr('href') or ''))
                        attribute = 'href'
                        pq(elem).replaceWith(new_elem)
                        elem = self.d('#%s' % id)
                        elem.attr('id', '')

                elif type == 'script':
                    asset = Script(base, ref, text=pq(elem).text())
                    if pq(elem).text():
                        has_text = True
                        # print(pq(elem))
                        id = uuid.uuid4().hex
                        new_elem = pq('<script id="%s" type="text/javascript" src="%s"></script>' % (id, pq(elem).attr('src') if pq(elem).attr('src') else ''))
                        attribute = 'src'
                        pq(elem).replaceWith(new_elem)
                        elem = self.d('#%s' % id)
                        elem.attr('id', '')
                else:
                    asset = Asset(base, ref)

                if not has_text:
                    asset = self.main_set.get(asset.getpath()) or asset


                self.main_set.add(asset)
                self.assets.add(asset)

                asset.main_set = self.main_set
                asset.dist = self.dist

                if not asset.saved_path:
                    asset.load()
                    asset.save(subfolder=subfolder)
                # print('***')
                # print(pq(elem))
                # print(attribute, os.path.relpath(asset.saved_path, self.saved_path).replace('../', './', 1))
                pq(elem).attr(attribute, os.path.relpath(asset.saved_path, self.saved_path).replace('../', './', 1))
                # print(pq(elem))
                self.text = self.d.outerHtml()
                self.save()

        super().parse_assets()

    def pages(self):
        if self.depth == self.max_depth:
            return
        pass
