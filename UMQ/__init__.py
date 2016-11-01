from __future__ import unicode_literals
import logging
from logging.handlers import RotatingFileHandler
import random
import subprocess
import youtube_dl
from flask import (Flask, flash, json, jsonify, request, Response, render_template, stream_with_context)
from flask_sqlalchemy import SQLAlchemy

app = Flask('__name__')
# app.register_blueprint(blueprint, url_prefix='/playlist')
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)

from UMQ.models import *


@app.route('/')
def index():
    '''Render tracklist.'''
    added = request.args.get('added', None)
    return render_template('index.html', added=added)


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
            pass
            app.logger.error(e)
        else:
            app.logger.info('Finished streaming')
            proc.kill()

    track = get(id)
    return Response(stream_with_context(ydl_stream(track['page_url'])),
                    mimetype='audio/mp4',
                    headers={'Accept-Ranges': 'bytes'})


@app.route('/playlist/info/<id>')
def get_track_info(id):
    track = get(id)
    return jsonify(track)


@app.route('/playlist', methods=['GET'])
def get_all_tracks():
    tracks = Track.query.all()
    app.logger.debug('%s track(s) found.' % len(tracks))
    if len(tracks) == 0:
        flash('Looks like you haven\'t added any tracks yet. Try this one:')
        flash(get_example())
    json_tracks = [t.to_json() for t in tracks]
    return json.dumps(json_tracks)


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
        new_track = Track(
            title=t['title'],
            artist=t.get('artist', ''),
            page_url=url,
            url=t.get('url', url)
            # TODO 'duration'=t.get('duration') somehow ???
        )
        new_id = add(new_track)
        app.logger.info('ADDED: %s (%s)' % t['title'] % new_id)
    return jsonify(title=t['title'], url=url)


# @app.route('/<id>', methods=['DELETE'])
# def delete(id=None):
#     '''Delete a track by ID.'''
#     res = g.playlist.find_one_and_delete({'_id': id})
#     app.logger.info('DELETED: %s - %s' % (res['title'], res['url']))
#     return json.dumps(res)


# TODO
# @app.route('/<id>', methods=['PUT'])
# def update(id):
#     track = request.get_json()
#     app.logger.debug(track)
#     res = g.playlist.update_one({'_id': track['id']}, track)
#     app.logger.debug(res)
#     return res

def add(track):
    try:
        db.session.add(track)
        db.session.commit()
        return track.id
    except:
        app.logger.error("Couldn't add to DB.")


def get(id):
    return Track.query.filter_by(id=id).first_or_404()


def get_all():
    return Track.query.all()


def get_example():
    return random.choice([
        'https://gloccamorradied.bandcamp.com/track/professional-confessional-2',
        'https://www.youtube.com/watch?v=CvCLhq8okxc',
        'https://soundcloud.com/serf-crook/homemovie02',
        'http://babydreamgirl.tumblr.com/post/137912267129/this-is-the-version-\f-beautiful-i-was-talking'
    ])


if __name__ == '__main__':
    if app.debug:
        handler = logging.StreamHandler()
        app.logger.addHandler(handler)
        app.logger.info('stream logger started')
    else:
        handler = RotatingFileHandler('logs/umq.log', maxBytes=10000, backupCount=1)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)

    app.run(debug=app.debug, port=5000, threaded=True)
