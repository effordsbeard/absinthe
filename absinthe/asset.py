from .assetset import AssetSet
from furl import furl
import uuid
import shutil
import os, os.path
import requests
from termcolor import colored
import copy


class Asset(object):

    def __init__(self, base='', ref='', check_url=lambda x: True, check_text=lambda x: True, dist=os.getcwd(), text=None, session=None, should_load=lambda x: True, ignore_query=True, prefix=''):
        self.base = base  # путь или ссылка, на которой была найдена ссылка на текущий ассет
        self.ref = ref  #  ссылка на ассет, которая найдена в другом файле

        # if ignore_query:
        #     self.ref = self.ref.split('?')[0]

        self.session = session if session else requests.Session()  # requests session
        self.raw = None  # бинарник файла
        self.text = text  # обычная текстовая версия файла, либо содержимое тега, который будет заменен ассетом
        self.prefix = prefix  # кусок пути который нужно проставлять перед сохранением
        self.name = uuid.uuid4().hex  # хеш который будет использоваться в базе для подстановки
        self.dist = dist
        self.check_url = check_url
        self.check_text = check_text
        self.subfolder = ''
        self.file_type = 'binary'

        if self.ref is None:
            self.ref = self.name

        try:
            self.src_name = self.ref.split('/')[-1]  # имя которое было у ассета до слития
        except:
            self.src_name = self.ref.split('/')[0]


        self.path = None
        self.f = None
        if not base.startswith('http'):
            self.path = os.path.join(base, ref)
        else:
            self.f = furl(base).join(ref)

        self.saved_path = None

        self.assets = AssetSet()  # другие ассеты, которые найдены в этом

        self.should_load = lambda: should_load(self)

    def getpath(self):
        if self.path:
            return self.path
        if self.f:
            return self.f.url

    def load(self, *args, **kwargs):
        if self.saved_path:
            return True

        if self.text:
            return True

        if self.path:
            return self.load_local(*args, **kwargs)
        if self.f:
            return self.download(*args, **kwargs)
        return False

    def download(self, method='GET', data={}, headers={}, log=True):
        if not self.should_load():
            return False

        # print('loading')
        if not self.f:
            if log:
                print(colored('Warning: downloading non http file, rejected.', 'yellow'))
            return False
        req = requests.Request(method, self.f.url, data=data, headers=headers)
        if not self.f.url.startswith('http'):
            return False
        prep_req = self.session.prepare_request(req)
        try:
            resp = self.session.send(prep_req)
            self.raw = resp.content
            self.text = resp.text
        except:
            if log:
                print(colored('Error was occured while downloading file:', 'red', attrs=['bold']), self.f.url)
            return False

        code_term = colored(resp.status_code, 'white', attrs=['bold'])

        if resp.status_code != 200:
            code_term = colored(resp.status_code, 'red', 'on_white', attrs=['bold'])

        if log:
            print(code_term, self.f.url)

        if resp.status_code != 200:
            return False

        return True

    def load_local(self, log=True):
        if not self.should_load():
            return False
        try:
            with open(self.f, 'rb') as f:
                self.raw = f.read()

            with open(self.f, 'r') as f:
                self.text = f.read()
        except:
            if log:
                print(colored('Error was occured while reading file:', 'red'), self.f)
            return False

        return True

    def save(self, subfolder='', name=None):
        if not subfolder and self.subfolder:
            subfolder = self.subfolder
        if subfolder:
            self.subfolder = subfolder
        name = name or self.src_name or self.name
        path = os.path.join(self.dist, subfolder)
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(path, name)
        self.saved_path = path

        if self.raw and self.file_type == 'binary':
            with open(path, 'wb') as f:
                f.write(self.raw)
                return True

        if self.text and self.file_type == 'text':
            with open(path, 'w') as f:
                f.write(self.text)
            return True

        print(colored('Warning: no data to save file:', 'yellow', attrs=['bold']), path)
        return False

    def parse_assets(self):
        # функция может быть реализована в дочерних классах по поиску других ассетов
        for asset in self.assets.assets:
            asset.parse_assets()
