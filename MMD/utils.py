# -*- encoding: utf-8 -*-

"""
Copied from
https://github.com/davidfischer-ch/pytoolbox/blob/master/pytoolbox/logging.py
"""

import logging
import re
from termcolor import colored
from os import path

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


def createfile(file_path, data):
    if not path.exists(file_path):
        with open(file_path, 'w') as config_file:
            config_file.write(data)