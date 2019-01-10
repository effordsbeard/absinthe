from .asset import Asset
import base64


class Image(Asset):

    def __init__(self, base, ref='', *args, **kwargs):
        super().__init__(base, ref, *args, **kwargs)
        self.file_type = 'binary'

        self.text = None
        if ref.startswith('data'):

            try:
                ext = ref.split(';')[0].split(':')[1].split('/')[1].split('+')[0].replace('base64', '')
            except:
                ext = ''
            self.text = None
            self.raw = base64.decodebytes(bytearray(ref.split(',')[1], encoding='utf-8'))
            self.name += '.' + ext
            self.src_name = None

    def parse_assets(self):
        pass
