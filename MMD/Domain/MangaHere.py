from MMD.Domain import domain
from MMD.utils import create_file, create_dir
from MMD.strings import *

import requests
from requests.exceptions import ConnectionError, ConnectTimeout, MissingSchema
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from threading import Thread
from queue import Queue
import os


class Downloader(domain.Downloader):
    DOMAIN = 'MangaHere'

    class ChapterDownloader(Thread):
        def __init__(self, id: int, chapter_queue: Queue, title: str, path: str, log):
            Thread.__init__(self)
            self.__id = id
            self.__chapter_queue = chapter_queue
            self.__title = title
            self.__path = os.path.join(path, title)
            self.__log = log

        @staticmethod
        def last_page(url:str):
            # TODO: Implement this
            page = requests.get(url=url).text
            soup = BeautifulSoup(page, Downloader.PARSER)
            return 0

        @staticmethod
        def download_image(url: str, path: str):
            page = requests.get(url=url).text
            soup = BeautifulSoup(page, Downloader.PARSER)
            img_url = soup.find(
                r'section',
                {r'class': r'read_img', r'id': r'viewer'}
            ).find(r'img', {r'id': 'image'}).get('src')
            urlretrieve(img_url, path)

        def run(self):
            while self.__chapter_queue.not_empty:
                url = self.__chapter_queue.get()
                chapter_number = url[url.rfind('/', 0, len(url)-1) + 1:-1]
                page = Downloader.ChapterDownloader.last_page(url=url)
                path = os.path.join(self.__path, chapter_number)
                meta_data_file = os.path.join(path, 'Downloaded.md')
                create_dir(path)
                if not os.path.exists(meta_data_file):
                    pages = [
                        (url + str(page_num) + '.html',
                         os.path.join(path, '{:03d}.jpg'.format(page_num)))
                        for page_num in range(1, page + 1)
                    ]
                    for page, image_path in pages:
                        retries = 0
                        while not os.path.exists(image_path):
                            try:
                                Downloader.ChapterDownloader.download_image(url=page, path=image_path)
                            except TimeoutError:
                                retries += 1
                                if retries > Downloader.MAX_RETRY:
                                    self.__log.error(THREAD_DOWNLOAD_FAILURE_MESSAGE.format(self.__id, image_path))
                                    break
                    # TODO: Check for complete download before writing to the meta-data-file.
                    with open(meta_data_file, mode='w') as f:
                        f.write(METADATA_FILE_CONTENT.format(self.__title, chapter_number, len(pages)))
                self.__chapter_queue.task_done()


    @staticmethod
    def download(url: str, threading: bool, log, path: str):
        log.debug(DOMAIN_MESSAGE.format(Downloader.DOMAIN))
        log.debug(METADATA_GATHER_MESSAGE.format(url))

        log.debug(TRY_ACCESSING_PAGE_MESSAGE)
        try:
            try:
                page = requests.get(url=url).text
            except MissingSchema:
                log.debug(MISSING_SCHEMA_MESSAGE.format(url))
                url = 'http://' + url
                log.debug(RETRYING_MESSAGE.format(url))
                page = requests.get(url=url).text
        except ConnectionError:
            log.debug(CONNECTION_ERROR_MESSAGE.format(url))
            log.info(EXIT_MESSAGE)
            quit(-1)

        title, cover, author, summary = Downloader.get_meta_data(page=page, log=log)
        log.info(METADATA_SUCCESS_MESSAGE)
        log.info(METADATA_MESSAGE.format(title, author, summary))

        chapters = Downloader.get_chapter_url(page=page, log=log)

        # Set-Up for multi threading
        thread_count = 4 if threading else 1
        chapter_threads = [Downloader.ChapterDownloader(
                                        id=i,
                                        chapter_queue=chapters,
                                        title=title,
                                        path=path, log=log)
                   for i in range(thread_count)]
        for chapter_thread in chapter_threads:
            chapter_thread.daemon = True
            # Start the Download process
            chapter_thread.start()
        chapters.join()

        log.info(DOWNLOAD_COMPLETE_MESSAGE)

    @staticmethod
    def get_chapter_url(page: str, log):

        soup = BeautifulSoup(page, Downloader.PARSER)

        chapter_anchors = soup.find(name='div',
                                    attrs={'class': 'detail_list'}).ul.find_all(name='a',
                                                                                attrs={'class': 'color_0077'})
        chapters = Queue()
        for chapter_anchor in reversed(chapter_anchors):
            chapters.put('http:' + chapter_anchor.get(r'href'))
        return chapters

    @staticmethod
    def get_meta_data(page: str, log):
        # Create the markup file
        soup = BeautifulSoup(page, Downloader.PARSER)

        # Now looking for Title
        log.debug(METADATA_SEARCH_TITLE)
        title = soup.find(name='h1',
                          attrs={'class': 'title'}).span.next_sibling
        title = title.title()
        log.debug(METADATA_SEARCH_SUCCESS_TITLE.format(title))

        # Now looking for Cover Image
        log.debug(METADATA_SEARCH_COVER)
        cover = soup.find(name='div',
                          attrs={'class': 'manga_detail_top clearfix'}).img.get(r'src')
        log.debug(METADATA_SEARCH_SUCCESS_COVER)

        # Now looking Author and Summary
        info_tag = soup.find(name='ul',
                             attrs={'class': 'detail_topText'})
        log.debug(METADATA_SEARCH_AUTHOR)
        for tag in info_tag.children:      # Go through the all info tags to find author tag
            if 'Author(s):' in str(tag):
                author = tag.a.string
                break
        log.debug(METADATA_SEARCH_SUCCESS_AUTHOR.format(author))

        log.debug(METADATA_SEARCH_SUMMARY)
        summary = str(info_tag.find(name='p',
                                    attrs={r'id': r'show'}))[35:-88]
        log.debug(METADATA_SEARCH_SUCCESS_SUMMARY.format(summary[:min(1000, len(summary))]))

        log.debug(METADATA_SUCCESS_MESSAGE)
        return title, cover, author, summary
    pass
