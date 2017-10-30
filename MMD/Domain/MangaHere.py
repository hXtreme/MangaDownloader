from MMD.Domain import domain
import requests
from requests.exceptions import ConnectionError, ConnectTimeout, MissingSchema
from bs4 import BeautifulSoup


class Downloader(domain.Downloader):
    DOMAIN = 'MangaHere'

    @staticmethod
    def download(url: str, threading: bool, log, path: str):
        log.debug('Domain set to {0}.'.format(Downloader.DOMAIN))
        log.debug('Gathering Meta-Data for the manga at: {0}'.format(url))

        log.debug('Trying to access the page.')
        try:
            page = requests.get(url=url).text
        except ConnectionError:
            log.debug('There was an error connecting to {0}.'.format(url))
            log.info('Exiting')
            quit(-1)
            pass
        except MissingSchema:
            log.debug('There was a MissingSchema Error while connecting to {0}'.format(url))
            url += 'http://'
            log.debug('Retrying with {0}'.format(url))
            try:
                page = requests.get(url=url).text
            except ConnectionError:
                log.debug('There was an error connecting to {0}.'.format(url))
                log.info('Exiting')
                quit(-1)
                pass
            pass

        title, cover, author, summary = Downloader.get_meta_data(page=page, log=log)
        pass

    @staticmethod
    def get_meta_data(page: str, log):

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
