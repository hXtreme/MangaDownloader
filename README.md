# MangaDownloader
Download Complete Manga with a single line!
This is a command line utility to download manga and meta-data from supported websites web-sites.


## System requirements

* Python3

## Instructions

### Installation
```
git clone https://github.com/hXtreme/MangaDownloader.git && cd scdl
python3 setup.py install
```

### Usage:
```
    mmd.py -h | --help
    mmd.py -v | --version
    mmd.py (--domain <domain-name>) (--url <url>) [-s | -o] [--threading] [--debug | --error] [--path]
```

### Options:
```
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
```

## README
The latest README file is available at:
```
https://github.com/hXtreme/MangaDownloader
```

## License

[GPL v2](https://www.gnu.org/licenses/gpl-2.0.txt), original author [hXtreme](https://github.com/hXtreme)
