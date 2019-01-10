from .asset import Asset


class Script(Asset):

    def __init__(self, base, ref='', *args, **kwargs):
        super().__init__(base, ref, *args, **kwargs)
        if self.src_name:
            if not '.' in self.src_name:
                self.src_name += '.js'
        self.name += '.js'
        self.file_type = 'text'

    def urls(self):
        pass  # любые ссылки
