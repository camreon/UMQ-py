import abc
import logging
import youtube_dl

from umq.log import log


class GenericStreamService(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def extract_info(self, url):
        pass


class MockStreamService(GenericStreamService):

    def extract_info(self, url):
        if 'album' in url:
            return [
                {
                    'title': 'mock title',
                    'alt_title': None,
                    'artist': 'mock artist',
                    'webpage_url': url,
                    'url': url + '-strean'
                },
                {
                    'title': None,
                    'alt_title': '',
                    'artist': 'mock artist 2',
                    'webpage_url': 'mock url 2',
                    'url': 'mock url 2-strean'

                },
                {
                    'title': 'mock alt title 3',
                    'artist': 'mock artist ',
                    'webpage_url': 'mock url 3',
                    'url': 'mock url 3-strean'

                }
            ]
        else:
            return [{
                'title': 'mock title',
                'artist': 'mock artist',
                'webpage_url': url,
                'url': url + '-strean'
            }]


class StreamService(GenericStreamService):

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def extract_info(self, url):
        """Returns list of track dicts from youtube-dl"""

        options = {
            'format': 'm4a/bestaudio',  # safari prefers m4a
            'logtostderr': True,
            'youtube_include_dash_manifest': False
            # fixes videos with unsupported adaptive stream type formats
            # https://github.com/ytdl-org/youtube-dl/issues/6099
        }

        log.info('Getting track info from youtube-dl for ' + url)

        with youtube_dl.YoutubeDL(options) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
            except youtube_dl.utils.YoutubeDLError as e:
                raise

        if 'entries' in info:
            tracks = info['entries']
        else:
            tracks = [info]

        log.info('Finished getting track info from youtube-dl for ' + url)

        return tracks
