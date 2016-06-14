from __future__ import unicode_literals

import logging
import random
import subprocess
import os

from logging.handlers import RotatingFileHandler
from flask import (Flask, Response, abort, flash, g, jsonify, redirect,
                   render_template, request, stream_with_context, url_for)
from flask.ext.pymongo import PyMongo

import youtube_dl


app = Flask('__name__')
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.secret_key = os.environ.get('SECRET_KEY', 'set by env var')
app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME', 'umq')
app.debug = True

mongo = PyMongo(app)


@app.before_request
def before_request():
    '''Connect to DB before every request.'''
    g.playlist = mongo.db.playlist


@app.route('/')
def index():
    '''Render tracklist.'''
    tracks = g.playlist.find().sort('_id', 1)
    if tracks.count() == 0:
        flash('Looks like you haven\'t added any tracks yet. Try this one:')
        flash(get_example())

    added = request.args.get('added_track_id', None)
    return render_template('index.jade', playlist=tracks, added_track_id=added)


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
            app.logger.error(type(e))
            app.logger.error(e)
        else:
            app.logger.info('Finished streaming')
            proc.kill()

    return Response(stream_with_context(ydl_stream(track['page_url'])),
                    mimetype='audio/mp4',
                    headers={'Accept-Ranges': 'bytes'})


@app.route('/playlist', methods=['POST'])
def add():
    '''Get track info from a URL and add it to the playlist.'''
    url = request.form['url']
    with youtube_dl.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)

    if 'entries' in info:
        tracks = info['entries']
    else:
        tracks = [info]

    for t in tracks:
        res = g.playlist.insert_one({
            'title': t['title'],
            'artist': t.get('artist', ''),
            'page_url': url,
            'url': t.get('url', url)
        })
        flash('ADDED: %s' % t['title'])
    return redirect(url_for('index', added_track_id=res.inserted_id))


@app.route('/delete/')
@app.route('/delete/<ObjectId:id>')
def delete(id=None):
    '''Delete a track by ID or delete all tracks.'''
    if id is None:
        result = g.playlist.delete_many({})
        flash('DELETED: %s tracks' % result.deleted_count)
    else:
        track = g.playlist.find_one_and_delete({'_id': id})
        flash('DELETED: %s - %s' % (track['title'], track['url']))
    return redirect(url_for('index'))


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
    handler = RotatingFileHandler('umq.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.run(debug=True, port=5000, threaded=True)
