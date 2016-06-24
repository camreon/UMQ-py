from __future__ import unicode_literals

import logging
import random
import subprocess
import os

from logging.handlers import RotatingFileHandler
from flask import (Flask, Response, abort, flash, g, json, jsonify,
                   render_template, request, stream_with_context)
from flask.ext.pymongo import PyMongo
from bson import json_util

import youtube_dl


app = Flask('__name__')
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.secret_key = os.environ.get('SECRET_KEY', 'set in .env')
app.config['MONGO_URI'] = os.environ.get('MONGODB_URI', 'mongodb://localhost/umq')
app.debug = True

mongo = PyMongo(app)


@app.before_request
def before_request():
    g.playlist = mongo.db.playlist


@app.route('/')
def index():
    '''Render tracklist.'''
    added = request.args.get('added', None)
    return render_template('index.jade', added=added)


@app.route('/playlist', methods=['GET'])
def get_all_tracks():
    tracks = list(g.playlist.find().sort('_id', 1))
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
        g.playlist.insert_one({
            'title': t['title'],
            'artist': t.get('artist', ''),
            'page_url': url,
            'url': t.get('url', url),
            # TODO 'duration': t.get('duration') ???
        })
        app.logger.info('ADDED: %s' % t['title'])
    return jsonify(title=t['title'], url=url)


@app.route('/playlist/<ObjectId:id>')
def stream_track(id):
    '''Get track URL based on ID and use youtube-dl to stream it.'''
    track = g.playlist.find_one_or_404(id)

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

    return Response(stream_with_context(ydl_stream(track['page_url'])),
                    mimetype='audio/mp4',
                    headers={'Accept-Ranges': 'bytes'})


@app.route('/playlist/<ObjectId:id>', methods=['DELETE'])
def delete(id=None):
    '''Delete a track by ID.'''
    res = g.playlist.find_one_and_delete({'_id': id})
    app.logger.info('DELETED: %s - %s' % (res['title'], res['url']))
    return json.dumps(res, default=json_util.default)


# TODO
@app.route('/playlist/<ObjectId:id>', methods=['PUT'])
def update(id):
    track = request.get_json()
    app.logger.debug(track)
    res = g.playlist.update_one({'_id': track['id']}, track)
    app.logger.debug(res)
    return res


# error handling #
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(400)
def custom400(error):
    app.logger.error(error)
    app.logger.error(error.description)
    abort(400, error.description)


def get_example():
    return random.choice([
        'https://gloccamorradied.bandcamp.com/track/professional-confessional-2',
        'https://www.youtube.com/watch?v=CvCLhq8okxc',
        'https://soundcloud.com/serf-crook/homemovie02',
        'http://babydreamgirl.tumblr.com/post/137912267129/this-is-the-version-\f-beautiful-i-was-talking'
    ])

# Run application
if __name__ == '__main__':
    handler = RotatingFileHandler('logs/umq.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.run(debug=True, port=5000, threaded=True)
