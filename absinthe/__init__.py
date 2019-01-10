import sys
import os, os.path
import pymist
import json
from .scraper import Scraper


def run():
    args = pymist.parse(sys.argv[1:])
    cwd = os.getcwd()
    lib_path = os.path.dirname(os.path.realpath(__file__))

    config_path = None if not args.get('c') else os.path.join(cwd, args.get('c'))
    config = {}

    if config_path:
        with open(config_path) as f:
            config = json.load(f)

    if not config.get('dist', '').startswith('/'):
        config['dist'] = os.path.join(cwd, config.get('dist', ''))

    if args.get('d'):
        config['dist'] = os.path.join(cwd, args.get('d'))

    source_type = 'remote'

    if args.get('s'):
        s = args.get('s')
        if s.startswith('http'):
            config['source'] = args.get('s')
        else:
            config['source'] = os.path.join(cwd, args.get('s'))
            source_type = 'local'

    if args.get('d'):
        config['depth'] = int(args.get('d'))

    if args.get('i'):
        config['index'] = args.get('i')

    if not config.get('source_type'):
        config['source_type'] = source_type

    if not config.get('depth'):
        config['depth'] = 0

    if not config.get('index'):
        config['index'] = ''

    if not config.get('dist_index'):
        config['dist_index'] = 'index.php'


    sc = Scraper(config)

    #
    # _ = args.get('_')
    # if not len(_):
    #     print('Expected command name. Please, use following format: "arrowstack <command> [args]')
    #     return
    # if _[0] == 'deploy':
    #     pass
        # docker.DockerClient()
