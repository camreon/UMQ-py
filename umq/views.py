import random

from flask import (
    Blueprint, flash, jsonify, request, Response, render_template
)
from umq.db import getAllTracks, getTrack, addTrack, deleteTrack, Track
from umq.log import log
from umq.stream_service import StreamService


bp = Blueprint("index", __name__)


@bp.route('/')
def index():
    """Render tracklist."""

    added = request.args.get('added', None)
    return render_template('index.html', added=added)


@bp.route('/playlist/<id>')
def stream_track(id, stream_service: StreamService):
    """Get track URL based on ID and use youtube-dl to stream it."""

    track = getTrack(id)

    try:
        return Response(
            # TODO: should use track.stream_url for playlists?
            stream_service.stream(track.page_url),
            mimetype='audio/mp3',
            headers={'Accept-Ranges': 'bytes'}
        )
    except Exception as e:
        log.error('Response error: {}'.format(str(e)))


@bp.route('/playlist/info/<id>')
def get_track_info(id):

    track = getTrack(id)
    return jsonify(track.to_json())


@bp.route('/playlist', methods=['GET'])
def get_all_tracks():

    tracks = getAllTracks()

    log.info('{} track(s) found.'.format(len(tracks)))

    if len(tracks) == 0:
        flash('Looks like you haven\'t added any tracks yet. Try this one:')
        flash(get_example())

    json_tracks = [t.to_json() for t in tracks]

    return jsonify(json_tracks)


@bp.route('/playlist', methods=['POST'])
def add(stream_service: StreamService):
    """Get track info from a URL and add it to the playlist."""

    data = request.get_json()
    url = data['page_url']
    info = stream_service.extract_info(url)

    if info and 'entries' in info:
        tracks = info['entries']
    else:
        tracks = [info]

    added_tracks = []

    for t in tracks:
        title = t.get('title')

        if title is None or title == '_':
            title = t.get('alt_title')

        new_track = Track(
            title=title,
            artist=t.get('artist'),
            page_url=url,
            stream_url=t.get('url', url)
            # TODO allow scrubbing. maybe by getting duration?
        )

        new_id = addTrack(new_track)
        added_tracks.append(new_track)

        log.info('ADDED: {0} (id: {1})'.format(title, new_id))

    return jsonify([t.to_json() for t in added_tracks])


@bp.route('/playlist/<id>', methods=['DELETE'])
def delete(id=None):
    """Delete a track by ID."""

    track = getTrack(id)
    deleteTrack(track)

    delete_message = 'DELETED: {0} - {1}'.format(track.title, track.page_url)
    log.info(delete_message)
    flash(delete_message)

    return jsonify(track.to_json())


# TODO
# @umq.route('/<id>', methods=['PUT'])
# def update(id):
#
#     track = request.get_json()
#     umq.logger.debug(track)
#     res = g.playlist.update_one({'_id': track['id']}, track)
#     umq.logger.debug(res)
#     return res=


def get_example():

    return random.choice([
        'https://gloccamorradied.bandcamp.com/track/professional-confessional-2',
        'https://www.youtube.com/watch?v=CvCLhq8okxc',
        'https://soundcloud.com/serf-crook/homemovie02'
    ])
