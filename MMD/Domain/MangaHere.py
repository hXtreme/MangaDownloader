from MMD.Domain import domain
from MMD.utils import create_file
import requests
from requests.exceptions import ConnectionError, ConnectTimeout, MissingSchema
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
            return 0

        @staticmethod
        def download_image(url: str, path: str):
            # TODO: Implement this
            pass

        def run(self):
            while True:
                url = self.__chapter_queue.get()
                chapter_number = url[url.rfind('/', 0, len(url)-1) + 1:-1]
                page = Downloader.ChapterDownloader.last_page(url=url)
                path = os.path.join(self.__path, chapter_number)
                meta_data_file = os.path.join(path, 'Downloaded.md')
                if not os.path.exists(meta_data_file) :
                    pages = ((url + str(page_num) + '.html', os.path.join(path, '{:03d}.jpg'.format(page_num))) for page_num in range(1, page + 1))
                    for page, image_path in pages:
                        retries = 0
                        while not os.path.exists(image_path):
                            try:
                                Downloader.ChapterDownloader.download_image(url=page, path=path)
                            except TimeoutError:
                                retries += 1
                                if retries > Downloader.MAX_RETRY:
                                    self.__log.error('Thread Id:{0} >> Failed to Download {1}'.format(self.__id, path))
                                    break
                    # TODO: Check for complete download before wirting to the meta-data-file.
                    with open(meta_data_file) as f:
                        f.write(
                            """# {0}
                            ## Details
                            ### Chapter No. :
                            ```
                            {1}
                            ```
                            ### Total Pages :
                            ```
                            {2}
                            ```
                            ## Pages
                            ```
                            <ADD ALL THE LINKS HERE>
                            ```
                            """.format(self.__title, chapter_number, len(pages))
                        )


    @staticmethod
    def download(url: str, threading: bool, log, path: str):
        log.debug('Domain set to {0}.'.format(Downloader.DOMAIN))
        log.debug('Gathering Meta-Data for the manga from: {0}'.format(url))

        log.debug('Trying to access the page.')
        try:
            try:
                page = requests.get(url=url).text
            except MissingSchema:
                log.debug('There was a MissingSchema Error while connecting to {0}'.format(url))
                url += 'http://'
                log.debug('Retrying with {0}'.format(url))
                page = requests.get(url=url).text
        except ConnectionError:
            log.debug('There was an ConnectionError while connecting to {0}.'.format(url))
            log.info('Exiting')
            quit(-1)

        title, cover, author, summary = Downloader.get_meta_data(page=page, log=log)
        log.debug('Title: {0}\nAuthor: {1}\nSummary: {2}'.format(title, author, summary))

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

        log.debug('The Manga should be downloaded!!')

    @staticmethod
    def get_chapter_url(page: str, log):

        soup = BeautifulSoup(markup=page, parser=Downloader.PARSER)

        chapter_anchors = soup.find(name='div',
                                    attrs={'class': 'detail_list'}).ul.find_all(name='a',
                                                                                attrs={'class': 'color_0077'})
        chapters = Queue()
        for chapter_anchor in reversed(chapter_anchors):
            chapters.put(chapter_anchor.get(r'href'))
        return chapters

    @staticmethod
    def get_meta_data(page: str, log):
        # Create the markup file
        soup = BeautifulSoup(markup=page, parser=Downloader.PARSER)

        # Now looking for Title
        log.debug('Now we are looking for the manga title.')
        title = soup.find(name='h1',
                          attrs={'class': 'title'}).span.next_sibling
        title = title.title()
        log.debug('Manga Title: {0}'.format(title))

        # Now looking for Cover Image
        log.debug('Now we are looking for the manga cover image.')
        cover = soup.find(name='div',
                          attrs={'class': 'manga_detail_top clearfix'}).img.get(r'src')
        log.debug('Successfully found the Cover Image')

        # Now looking Author and Summary
        info_tag = soup.find(name='ul',
                             attrs={'class': 'detail_topText'})
        log.debug('Now looking for Author')
        for tag in info_tag.children:      # Go through the all info tags to find author tag
            if 'Author(s):' in str(tag):
                author = tag.a.string
                break
        log.debug('Author: {0}'.format(author))

        log.debug('Now looking for Summary Text')
        summary = str(info_tag.find(name='p',
                                    attrs={r'id': r'show'}))[35:-88]
        log.debug('Summary (at most first 1000 chars): {0}'.format(summary[:min(1000, len(summary))]))

        log.info('Successfully Gathered all the meta-data for {0}'.format(title))
        return title, cover, author, summary
    pass
