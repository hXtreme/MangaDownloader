# -*- encoding: utf-8 -*-

"""Python Manga Downloader (MyMangaDownloader)."""

from os import path, environ, makedirs
from MMD.utils import create_file

__version__ = 'v0.0.1'


config_dir = path.join(path.expanduser('~'), 'MMD\.config')
if 'XDG_CONFIG_HOME' in environ:
    config_dir = environ['XDG_CONFIG_HOME']

if not path.exists(config_dir):
    makedirs(config_dir)

# LOG_PATH = 'MMD.log'
LOG_PATH = path.join(config_dir, 'MMD.log')
CONFIG_PATH = path.join(config_dir, 'MMD.cfg')
text = """[MMD]
path = {0}

""".format(path.join(path.expanduser('~'), 'MMD\Library'))

create_file(CONFIG_PATH, text)
create_file(LOG_PATH, '')
