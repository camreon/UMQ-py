from __future__ import unicode_literals

import argparse
import youtube_dl
import logging

parser = argparse.ArgumentParser(description='stream audio via youtube-dl')
parser.add_argument(dest='url')
args = parser.parse_args()

logger = logging.getLogger('ydl')
logger.addHandler(logging.StreamHandler())
logging.info('YDL streaming %s' % args.url)

ydl_opts = {
    'format': 'mp3/bestaudio/best',
    'outtmpl': '-',  # stream to stdout
    'logger': logger,
    'logtostderr': True,
    'verbose': True,
    'debug_printtraffic': True
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([args.url])
