from __future__ import unicode_literals

import argparse
import youtube_dl
import logging

handler = logging.StreamHandler()
logger = logging.getLogger('ydl')
logger.addHandler(handler)
logger.info('YDL stream startup')

parser = argparse.ArgumentParser(description='stream audio via youtube-dl')
parser.add_argument(dest='url')

args = parser.parse_args()

ydl_opts = {
    'format': 'mp4/bestaudio/best',
    'outtmpl': '-',  # stream to stdout
    'logger': logger
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([args.url])
