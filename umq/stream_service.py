import abc
import logging
import youtube_dl
import subprocess

from flask import stream_with_context
from umq.log import log


class GenericStreamService(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def extract_info(self, url):
        pass

    @stream_with_context
    @abc.abstractmethod
    def stream(self, url):
        pass


class MockStreamService(GenericStreamService):

    def extract_info(self, url):
        if 'album' in url:
            return {
                'entries': [
                    {
                        'title': 'mock title',
                        'alt_title': None,
                        'artist': 'mock artist',
                        'page_url': url
                    },
                    {
                        'title': None,
                        'alt_title': '',
                        'artist': 'mock artist 2',
                        'page_url': 'mock url 2'
                    },
                    {
                        'title': '_',
                        'alt_title': 'mock alt title 3',
                        'artist': 'mock artist ',
                        'page_url': 'mock url 3'
                    }
                ]
            }
        else:
            return {
                'title': 'mock title',
                'artist': 'mock artist',
                'page_url': url
            }

    def stream(self, url):
        from io import BytesIO

        mock_stream = BytesIO(b'\x64\x00\x80\x00\x00\x00\x09\x00\x47\x65\x6E\x50\x61\x72\x61\x6D\x73\x00\x6E\x00\x18'
                              b'\x00\x00\x00\x53\x75\x70\x50\x61\x72\x61\x6D\x73\x00\x64\x00\x3B\x00\x00\x00\x46\x78'
                              b'\x64\x50\x61\x72\x61\x6D\x73\x00\x6E\x00\x36\x00\x00\x00\x4B\x65\x79\x45\x76\x65\x6E'
                              b'\x74\x73\x00\x6E\x00\x90\x00\x00\x00\x44\x61\x74\x61\x50\x74\x73\x00\x64\x00\xAE\x86'
                              b'\x01\x00\x41\x52\x53\x70\x65\x63\x69\x61\x6C\x00\x6E\x00\x16\x02\x00\x00\x41\x52\x45'
                              b'\x76\x65\x6E\x74\x00\x64\x00\xCE\x00\x00\x00\x43\x6B\x73\x75\x6D\x00\x64\x00\x02\x00'
                              b'\x00\x00')

        yield mock_stream


class StreamService(GenericStreamService):

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.addHandler(logging.StreamHandler())

        self.options = {
            'format': 'mp3/bestaudio/best',
            'logger': self.logger,
            'verbose': True,
        }

    def extract_info(self, url):

        try:
            with youtube_dl.YoutubeDL(self.options) as ydl:
                return ydl.extract_info(url, download=False)
        except Exception as e:
            self.logger.error(str(e))

    @stream_with_context
    def stream(self, url):

        log.info('YDL started streaming %s' % url)

        try:
            proc = subprocess.Popen(['python', 'umq/ydl_stream.py', url],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    bufsize=0)
            for line in proc.stdout:
                yield line
        except (Exception, OSError) as e:
            log.error('Streaming error: {}'.format(str(e)))
            proc.kill()
        else:
            log.info('Finished streaming %s' % url)
            proc.kill()

        # TODO: use ydl directly here instead of via umq/ydl_stream.py
        # stream_options = self.options
        # stream_options['outtmpl'] = '-'  # streams to stdout

        # with youtube_dl.YoutubeDL(stream_options) as ydl:
        #     ydl.download(url)
