import random

from flask import (
    abort, Blueprint, flash, jsonify, request, render_template
)
from umq.db import getAllTracks, getTrack, addTrack, deleteTrack, Track
from umq.log import log
from umq.errors import JsonException
from umq.stream_service import StreamService


bp = Blueprint("index", __name__)


@bp.route('/')
def index():
    """Render tracklist."""

    added = request.args.get('added', None)
    return render_template('index.html', added=added)


@bp.route('/playlist/<id>')
def get_track_info(id, stream_service: StreamService):
    """Update track info from youtube-dl every time db is queried """

    track = getTrack(id)

    try:
        tracks = stream_service.extract_info(track.page_url)
    except Exception as error:
        abort(400, error)

    track = Track.from_dict(tracks[0])
    track.id = id

    return jsonify(track.to_json())


@bp.route('/playlist/', methods=['GET'])
def get_all_tracks():

    tracks = getAllTracks()

    log.info('{} track(s) found.'.format(len(tracks)))

    if len(tracks) == 0:
        flash('Looks like you haven\'t added any tracks yet. Try this one:')
        flash(get_example())

    json_tracks = [t.to_json() for t in tracks]

    return jsonify(json_tracks)


@bp.route('/playlist/', methods=['POST'])
def add(stream_service: StreamService):
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
            stream_url=t.get('url', url)
        )

        new_id = addTrack(new_track)
        added_tracks.append(new_track)

        log.info('ADDED: {0} (id: {1})'.format(t.get('title'), new_id))

    return jsonify([t.to_json() for t in added_tracks])


@bp.route('/playlist/<id>', methods=['DELETE'])
def delete(id=None):
    """Delete a track by ID."""

    track = getTrack(id)
    deleteTrack(track)

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

    # want both the youtube-dl error and url here

    json_exception = JsonException(error.description.args[0])

    response = jsonify(json_exception.to_dict())
    response.status_code = json_exception.status_code

    return response
