# MangaDownloader
A command line utility to download manga and meta-data from web-sites.


## System requirements

* Python3

## Instructions

### Installation
```
git clone https://github.com/hXtreme/MangaDownloader.git && cd scdl
python3 setup.py install
```

### Options:
```
   -h -help                 Show this screen
   -v -version              Show the version information
   -domain [domain-name]    The domain from where you want to download; valid parameters are: MangaHere, KissManga, MangaPanda.
   -url [url]               URL must be from the provided domain and must be the summary page of the desired manga
   -mode [ o | s ]          Overwrite \ Skip existing files
   -threading               Download via multiple threads (Shows promise of performance boost)
```
## License

[GPL v2](https://www.gnu.org/licenses/gpl-2.0.txt), original author [hXtreme](https://github.com/hXtreme)
