from __future__ import unicode_literals

import argparse
import youtube_dl
import logging

handler = logging.StreamHandler()
logger = logging.getLogger('ydl')
logger.addHandler(handler)
logger.info('YDL stream startup')

# parser = argparse.ArgumentParser(description='stream audio via youtube-dl')
# parser.add_argument(dest='url')

# args = parser.parse_args()

ydl_opts = {
    'format': 'mp4/bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    # 'outtmpl': '-',  # stream to stdout
    'outtmpl': 'download/%(title)s.%(ext)s',
    'logger': logger,
    'verbose': True

}

with open('downloads_video/urls.txt', 'r') as f:
    urls = f.read().split()

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    for url in urls:
        print('Downloading: ', url)
        ydl.download([url])  # args.url
