'''
This file contains all the strings that are used by MMD.
Translate as desired!
'''

APP_NAME = 'Manga Downloader'


UNSUPPORTED_DOMAIN_MESSAGE = 'Unsupported Domain: {0}'
DOMAIN_MESSAGE = 'Domain set to {0}.'

TRY_ACCESSING_PAGE_MESSAGE = 'Trying to access the page.'

METADATA_GATHER_MESSAGE = 'Gathering Meta-Data for the manga from: {0}'
METADATA_SEARCH_TITLE = 'Now looking for the title.'
METADATA_SEARCH_COVER = 'Now looking for the cover image.'
METADATA_SEARCH_AUTHOR = 'Now looking for the Author'
METADATA_SEARCH_SUMMARY = 'Now looking for Summary Text'

METADATA_SEARCH_SUCCESS_TITLE = 'Manga Title: {0}'
METADATA_SEARCH_SUCCESS_COVER = 'Successfully found the Cover Image'
METADATA_SEARCH_SUCCESS_AUTHOR = 'Author: {0}'
METADATA_SEARCH_SUCCESS_SUMMARY = 'Summary (at most first 1000 chars): {0}'

METADATA_SUCCESS_MESSAGE = 'Successfully collected the meta-data.'
METADATA_MESSAGE = 'Title: {0}\nAuthor: {1}\nSummary: {2}'

DOWNLOAD_STARTED_MESSAGE = 'The Manga should be downloaded!!'

THREAD_FAILURE_MESSAGE = 'Thread Id:{0} >> Failed to Download {1}'
METADATA_FILE_CONTENT = '# {0}\n' \
                        '## Details\n' \
                        '### Chapter No. :\n' \
                        '```\n' \
                        '{1}\n' \
                        '```\n' \
                        '### Total Pages :\n' \
                        '```\n' \
                        '{2}\n' \
                        '```\n' \
                        '## Pages\n' \
                        '```\n' \
                        '<ADD ALL THE LINKS HERE>\n' \
                        '```\n' \
                        '---\n' \
                        'File made by [MMD](https://github.com/hXtreme/MangaDownloader)\n'


MISSING_SCHEMA_MESSAGE = 'There was a MissingSchema Error while connecting to {0}. ' \
                         'This usually signifies that we are missing "https://" at the beginning of the url.'
CONNECTION_ERROR_MESSAGE = 'There was an ConnectionError while connecting to {0}.'


RETRYING_MESSAGE = 'Retrying with {0}'

EXIT_MESSAGE = 'Exiting'
