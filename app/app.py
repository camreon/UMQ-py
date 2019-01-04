from __future__ import unicode_literals
import logging
import random
import subprocess
import youtube_dl

from flask import (
    Flask, flash, json, jsonify, request, Response, render_template, stream_with_context
)
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)

log_handler = logging.StreamHandler()
app.logger.addHandler(log_handler)


class Track(db.Model):
    __tablename__ = 'tracks'

    id = db.Column(db.Integer, primary_key=True)
    stream_url = db.Column(db.String())
    title = db.Column(db.String())
    artist = db.Column(db.String())
    page_url = db.Column(db.String())

    def __init__(self, stream_url, title, artist, page_url):
        self.stream_url = stream_url
        self.title = title
        self.artist = artist
        self.page_url = page_url

    def __repr__(self):
        return '{}'.format(self.id)

    def to_json(self):
        return dict(
            id=self.id,
            stream_url=self.stream_url,
            title=self.title,
            artist=self.artist,
            page_url=self.page_url
        )


@app.route('/')
def index():
    '''Render tracklist.'''
    added = request.args.get('added', None)
    return render_template('index.html', added=added)


def ydl_stream(url):
    try:
        app.logger.info('Started streaming %s' % url)
        proc = subprocess.Popen(['python', 'ydl_stream.py', url],
                                stdout=subprocess.PIPE,
                                bufsize=0)
        for line in proc.stdout:
            yield line
    except IOError as e:
        app.logger.error(str(e))
    else:
        app.logger.info('Finished streaming')
        proc.kill()


@app.route('/playlist/<id>')
def stream_track(id):
    '''Get track URL based on ID and use youtube-dl to stream it.'''
    track = getTrack(id)
    return Response(stream_with_context(ydl_stream(track.page_url)),
                    mimetype='audio/mp4',
                    headers={'Accept-Ranges': 'bytes'})


@app.route('/playlist/info/<id>')
def get_track_info(id):
    track = getTrack(id)
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
            stream_url=t.get('url', url)
            # TODO 'duration'=t.get('duration') somehow ???
        )
        new_id = addTrack(new_track)
        app.logger.info('ADDED: %s (%s)' % (t['title'], new_id))
    return jsonify(title=t['title'], url=url)


@app.route('/<id>', methods=['DELETE'])
def delete(id=None):
    '''Delete a track by ID.'''
    track = Track.query.get(id)
    deleteTrack(track)
    app.logger.info('DELETED: %s - %s' % (track.title, track.url))
    return json.dumps(track)


# TODO
# @umq.route('/<id>', methods=['PUT'])
# def update(id):
#     track = request.get_json()
#     umq.logger.debug(track)
#     res = g.playlist.update_one({'_id': track['id']}, track)
#     umq.logger.debug(res)
#     return res

def addTrack(track):
    try:
        db.session.add(track)
        db.session.commit()
        return track.id
    except:
        app.logger.error("Error adding track to DB.")


def deleteTrack(track):
    try:
        db.session.delete(track)
        db.session.commit()
    except:
        app.logger.error("Error deleting track from DB.")


def getTrack(id):
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
