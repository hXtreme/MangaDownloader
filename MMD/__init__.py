# -*- encoding: utf-8 -*-

"""Python Manga Downloader (MyMangaDownloader)."""

from os import path, environ, makedirs

__version__ = 'v0.0.1'


def createfile(file_path, data):
    if not path.exists(file_path):
        with open(file_path, 'w') as config_file:
            config_file.write(data)

config_dir = path.join(path.expanduser('~'), '.config\MMD')
if 'XDG_CONFIG_HOME' in environ:
    config_dir = environ['XDG_CONFIG_HOME']

if not path.exists(config_dir):
    makedirs(config_dir)

# LOG_PATH = 'MMD.log'
LOG_PATH = path.join(config_dir, 'MMD.log')
CONFIG_PATH = path.join(config_dir, 'MMD.cfg')
text = """[MMD]
path = .
"""

createfile(CONFIG_PATH, text)
createfile(LOG_PATH, '')
