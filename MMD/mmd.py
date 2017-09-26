#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

""" MyMangaDownloader(mmd) allows you to download Complete Manga

Usage:  mmd.py -h | --help
        mmd.py -v | --version
        mmd.py (--domain <domain-name>) (--url <url>) [-s | -o]\
         [--threading] [--debug | --error] [--path]


    -h --help                Show this screen
    --version                Show the version information
    --domain <domain-name>   The domain from where you want to download; valid parameters are: MangaHere, KissManga, MangaPanda.
    --url <url>              URL must be from the provided domain and must be the summary page of the desired manga
    -o                       Overwrite existing files
    -s                       Skip existing files
    --path                   Save path (must exist before-hand)
    --threading              Download via multiple threads (Shows promise of performance boost)
    --error                  Set logging priority to error
    --debug                  Set logging priority to debug

"""


from logging import WARNING, ERROR, INFO, DEBUG, basicConfig as log_config, getLogger as get_logger
from configparser import ConfigParser
import os
from signal import signal, SIGINT
from docopt import docopt


from MMD import __version__, CONFIG_PATH, LOG_PATH
from MMD.utils import ColorizeFilter
from MMD.Domain import domain, MangaHere

# Supported Domains
DOMAINS = {'MangaHere': MangaHere.Downloader}

# SetUp the logger
log_config(level=INFO, format='%(message)s', filename=LOG_PATH)
get_logger('requests').setLevel(WARNING)
log = get_logger(__name__)
log.setLevel(INFO)
log.addFilter(ColorizeFilter())

# SetUp the ConfigParser
config = ConfigParser()
config.read(CONFIG_PATH)

# Argument ID's
DOMAIN_ID = '--domain'
URL_ID = '--url'
PATH_ID = '--path'
THREADING_ID = '--threading'
DEBUG_ID = '--debug'
ERROR_ID = '--error'

arguments = dict()
downloader = domain.Downloader
path = config.get('MMD', 'path')
url = str()


def main():
    # Set-Up to use global variables
    global arguments

    # Parse Arguments
    arguments = docopt(__doc__, version=__version__)

    if arguments[DEBUG_ID]:
        log.level = DEBUG
    elif arguments[ERROR_ID]:
        log.level = ERROR

    log.info('Manga Downloader')
    log.debug(arguments)

    setup_parameters()

    downloader.download(url=arguments[URL_ID],
                        threading=arguments[THREADING_ID],
                        log=log,
                        path=path)


    pass


def setup_parameters():
    # Set-Up to use global variables
    global downloader, path

    if arguments[DOMAIN_ID] not in DOMAINS:
        log.debug('Unsupported Domain: {0}'.format(arguments[DOMAIN_ID]))
        quit()
    downloader = DOMAINS[arguments[DOMAIN_ID]]
    if PATH_ID in arguments:
        path = arguments[PATH_ID]
    pass

if __name__ == '__main__':
    main()
