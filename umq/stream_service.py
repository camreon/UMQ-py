import abc
import logging
import youtube_dl


class GenericStreamService(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def extract_info(self, url):
        pass

    @abc.abstractmethod
    def stream(self, url):
        pass


class MockStreamService(GenericStreamService):

    def extract_info(self, url):
        return [
            {
                'title': 'mock title',
                'artist': 'mock artist',
                'url': 'mock url'
            },
            {
                'title': 'mock title 2',
                'artist': 'mock artist 2',
                'url': 'mock url 2'
            }
        ]

    def stream(self, url):
        return None


class StreamService(GenericStreamService):

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.addHandler(logging.StreamHandler())

        self.options = {
            'format': 'mp4/bestaudio/best',
            'logger': self.logger,
            'logtostderr': True,
            'verbose': True,
            'debug_printtraffic': True,
            'simulate': True
        }

    def extract_info(self, url):

        try:
            with youtube_dl.YoutubeDL(self.options) as ydl:
                return ydl.extract_info(url, download=False)
        except Exception as e:
            self.logger.error(str(e))

    def stream(self, url):

        self.logger.info('YDL streaming %s' % url)

        stream_options = self.options
        stream_options['outtmpl'] = '-'  # streams to stdout

        with youtube_dl.YoutubeDL(stream_options) as ydl:
            ydl.download(url)
