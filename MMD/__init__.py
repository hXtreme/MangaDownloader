# -*- encoding: utf-8 -*-

"""Python Manga Downloader (MyMangaDownloader)."""

from os import path, environ, makedirs

__version__ = 'v0.0.1'

config_dir = path.join(path.expanduser('~'), '.config/MMD')
if 'XDG_CONFIG_HOME' in environ:
    config_dir = environ['XDG_CONFIG_HOME']

config_file_path = path.join(config_dir, 'MMD.cfg')
text = """[MMD]
auth_token =
path = .
"""

if not path.exists(config_dir):
    makedirs(config_dir)

if not path.exists(config_file_path):
    with open(config_file_path, 'w') as f:
        f.write(text)
