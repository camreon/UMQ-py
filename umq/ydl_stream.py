from __future__ import unicode_literals

import argparse
import youtube_dl

from umq.log import log

parser = argparse.ArgumentParser(description='stream audio via youtube-dl')
parser.add_argument(dest='url')
args = parser.parse_args()


def error_hook(status):
    if status['status'] == 'error':
        log.error('YDL error streaming {}'.format(status['filename']))


ydl_opts = {
    'format': 'mp3/bestaudio/best',
    'outtmpl': '-',  # stream to stdout
    'logger': log,
    'progress_hooks': [error_hook],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([args.url])
