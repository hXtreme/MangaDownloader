#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

import MMD

setup(
    name='MyMangaDownloader',
    version=MMD.__version__,
    packages=find_packages(),
    author='hXtreme',
    author_email='harsh.xtremepro@outlook.com',
    description='Download Complete Manga with a single line.',
    long_description="README on github : https://github.com/hXtreme/MangaDownloader",
    install_requires=[
        'docopt',
        'requests',
        'clint',
        'termcolor',
    ],
    url='https://github.com/hXtreme/MangaDownloader',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 5 - Production/Stable',
        'License :: :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet',
        'Topic :: Multimedia :: Images/Photos',
        'Topic :: Multimedia :: Comics/Manga',
    ],
    entry_points={
        'console_scripts': [
            'MMD = MMD.mmd:main',
            'MyMangaDownloader = MMD.mmd:main',
            'MangaDownloader = MMD.mmd:main',
            'mmd = MMD.mmd:main',
        ],
    },
)
