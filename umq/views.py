import random

from flask import (
    abort, Blueprint, flash, jsonify, request, render_template, redirect
)
from umq.db import Track, Playlist
from umq.log import log
from umq.errors import JsonException
from umq.stream_service import StreamService


bp = Blueprint("index", __name__)


@bp.route('/')
@bp.route('/<id>')
def index(id=1):
    """Render tracklist."""

    added = request.args.get('added', None)
    return render_template('index.html', added=added)


@bp.route('/playlist/<id>/<track_id>')
def get_track_info(id, track_id, stream_service: StreamService):
    """Update track info from youtube-dl every time db is queried """

    track = Track.get(track_id)

    try:
        tracks = stream_service.extract_info(track.page_url)
    except Exception as error:
        abort(400, error)

    track = Track.from_dict(tracks[0])
    track.id = track_id

    return jsonify(track.to_json())


@bp.route('/playlist/', methods=['GET'])
@bp.route('/playlist/<id>', methods=['GET'])
def get_playlist_tracks(id=1):

    tracks = Playlist.getTracks(id)

    log.info('{} track(s) found.'.format(len(tracks)))

    if len(tracks) == 0:
        Playlist.add()

        flash('Looks like you haven\'t added any tracks yet. Try this one:')
        flash(get_example())

    json_tracks = [t.to_json() for t in tracks]

    return jsonify(json_tracks)


@bp.route('/newplaylist/')
def add_playlist():

    new_id = Playlist.query.count() + 1

    return redirect('/{}'.format(new_id))


@bp.route('/playlist/', methods=['POST'])
@bp.route('/playlist/<id>', methods=['POST'])
def add(stream_service: StreamService, id=1):
    """Get track info from a URL and add it to the playlist."""

    data = request.get_json()
    url = data['page_url'].strip()

    try:
        tracks = stream_service.extract_info(url)
    except Exception as error:
        abort(400, error)

    added_tracks = []

    for t in tracks:
        new_track = Track(
            title=t.get('title'),
            artist=t.get('artist'),
            page_url=url,
            stream_url=t.get('url', url),
            playlist_id=id
        )

        new_id = Track.add(new_track)
        added_tracks.append(new_track)

        log.info('ADDED: {0} (id: {1})'.format(t.get('title'), new_id))

    return jsonify([t.to_json() for t in added_tracks])


@bp.route('/playlist/<id>/<track_id>', methods=['DELETE'])
def delete(id=None, track_id=None):
    """Delete a track by ID."""

    track = Track.get(track_id)
    Track.delete(track)

    log.info('DELETED: {0} - {1}'.format(track.title, track.page_url))

    return jsonify(track.to_json())


def get_example():

    return random.choice([
        'https://gloccamorradied.bandcamp.com/track/professional-confessional-2',
        'https://www.youtube.com/watch?v=CvCLhq8okxc',
        'https://soundcloud.com/serf-crook/homemovie02'
    ])


@bp.app_errorhandler(400)
def custom400(error):
    log.error(error)

    #TODO: want both the youtube-dl error and url here

    json_exception = JsonException(error.description.args[0])

    response = jsonify(json_exception.to_dict())
    response.status_code = json_exception.status_code

    return response
