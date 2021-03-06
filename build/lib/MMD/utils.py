# -*- encoding: utf-8 -*-

"""
Partly copied from:
    https://github.com/davidfischer-ch/pytoolbox/blob/master/pytoolbox/logging.py
"""

import logging
import re
from termcolor import colored
from os import path, mkdir

__all__ = ('ColorizeFilter', )


class ColorizeFilter(logging.Filter):

    color_by_level = {
        logging.DEBUG: 'yellow',
        logging.ERROR: 'red',
        logging.INFO: 'white'
    }

    def filter(self, record):
        record.raw_msg = record.msg
        color = self.color_by_level.get(record.levelno)
        if color:
            record.msg = colored(record.msg, color)
        return True


def create_file(file_path, data):
    if not path.exists(file_path):
        with open(file_path, 'w') as config_file:
            config_file.write(data)


def create_dir(location: str):
    directory = path.dirname(location)
    if directory > '' and not path.exists(directory):
        mkdir(directory)
    if location is not None and location > '' and not path.exists(location):
        mkdir(location)
