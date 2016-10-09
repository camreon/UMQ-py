from flask import (flash, json, jsonify, request, Response, stream_with_context)
from bson import json_util
import subprocess
import random
import youtube_dl
from app import app
from models import Track

playlistBlueprint = Blueprint('playlistBlueprint', __name__)


@app.route('/playlist/<id>')
def stream_track(id):
    '''Get track URL based on ID and use youtube-dl to stream it.'''
    def ydl_stream(url):
        try:
            app.logger.info('Streaming %s' % url)
            proc = subprocess.Popen(['python', 'ydl_stream.py', url],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,
                                    bufsize=0)
            for line in proc.stdout:
                yield line
        except (OSError, Exception, BaseException) as e:
            app.logger.error(e)
        else:
            app.logger.info('Finished streaming')
            proc.kill()

    track = Track.get(id)
    return Response(stream_with_context(ydl_stream(track['page_url'])),
                    mimetype='audio/mp4',
                    headers={'Accept-Ranges': 'bytes'})


@app.route('/playlist/info/<id>')
def get_track_info(id):
    track = Track.get(id)
    return jsonify(track)


@app.route('/playlist', methods=['GET'])
def get_all_tracks():
    tracks = Track.query.all()
    app.logger.debug('%s track(s) found.' % len(tracks))
    if len(tracks) == 0:
        flash('Looks like you haven\'t added any tracks yet. Try this one:')
        flash(get_example())
    return json.dumps(tracks, default=json_util.default)


@app.route('/playlist', methods=['POST'])
def add():
    '''Get track info from a URL and add it to the playlist.'''
    data = request.get_json()
    url = data['url']
    try:
        with youtube_dl.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
    except:
        # TODO handle unsupported URLs
        info = {'url': url, 'title': 'n/a'}  # offline dummy data

    tracks = info['entries'] if 'entries' in info else [info]
    for t in tracks:
        Track.add(Track(
            t['title'],
            t.get('artist', ''),
            url,
            t.get('url', url)
            # TODO 'duration'=t.get('duration') somehow ???
        ))
        app.logger.info('ADDED: %s' % t['title'])
    return jsonify(title=t['title'], url=url)


# @app.route('/playlist/<id>', methods=['DELETE'])
# def delete(id=None):
#     '''Delete a track by ID.'''
#     res = g.playlist.find_one_and_delete({'_id': id})
#     app.logger.info('DELETED: %s - %s' % (res['title'], res['url']))
#     return json.dumps(res, default=json_util.default)


# TODO
# @app.route('/playlist/<id>', methods=['PUT'])
# def update(id):
#     track = request.get_json()
#     app.logger.debug(track)
#     res = g.playlist.update_one({'_id': track['id']}, track)
#     app.logger.debug(res)
#     return res


def get_example():
    return random.choice([
        'https://gloccamorradied.bandcamp.com/track/professional-confessional-2',
        'https://www.youtube.com/watch?v=CvCLhq8okxc',
        'https://soundcloud.com/serf-crook/homemovie02',
        'http://babydreamgirl.tumblr.com/post/137912267129/this-is-the-version-\f-beautiful-i-was-talking'
    ])
