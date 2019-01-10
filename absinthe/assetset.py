class AssetSet(object):

    def __init__(self):
        self.assets = []

    def add(self, asset):
        if not self.has(asset):
            self.assets.append(asset)

    def has(self, asset):
        for _asset in self.assets:
            if asset.getpath() == _asset.getpath():
                return True

        return False

    def get(self, path):
        for asset in self.assets:
            if asset.getpath() == path:
                return asset
        return None
