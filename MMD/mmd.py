#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

""" MyMangaDownloader(mmd) allows you to download Complete Manga

Usage:  mmd.py -h | --help
        mmd.py -v | --version
        mmd.py (--domain <domain-name>) (--url <url>) [-s | -o]\
         [--threading] [--debug | --error]


    -h --help                Show this screen
    -v --version             Show the version information
    --domain <domain-name>   The domain from where you want to download; valid parameters are: MangaHere, KissManga, MangaPanda.
    --url <url>              URL must be from the provided domain and must be the summary page of the desired manga
    -o                       Overwrite existing files
    -s                       Skip existing files
    --path                   Save path (must exist before-hand)
    --threading              Download via multiple threads (Shows promise of performance boost)
    --error                  Set logging priority to error
    --debug                  Set logging priority to debug

"""

from logging import WARNING, ERROR, INFO, DEBUG, info, basicConfig as log_config, getLogger
import os
from signal import signal, SIGINT
from docopt import docopt
from MMD import __version__



log_config(level=INFO, format='%(message)s')
getLogger('requests').setLevel(WARNING)
log = getLogger(__name__)
log.setLevel(INFO)
log.addFilter(utils.ColorizeFilter())


arguments = None


def main():
    # SetUp to use global variables
    global arguments

    # Parse Arguments
    arguments = docopt(__doc__, version=__version__)
    pass


if __name__ == '__main__':
    main()
