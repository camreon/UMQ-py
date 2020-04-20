import json

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from umq.log import log


db = SQLAlchemy()


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

    @staticmethod
    def from_dict(track_dict):
        track = Track(
            title=track_dict.get('title'),
            artist=track_dict.get('artist'),
            page_url=track_dict.get('webpage_url'),
            stream_url=track_dict.get('url')
        )

        return track


def addTrack(track):
    try:
        db.session.add(track)
        db.session.commit()
        return track.id
    except SQLAlchemyError as e:
        log.error("Error adding track -- %s" % str(e))


def deleteTrack(track):
    try:
        db.session.delete(track)
        db.session.commit()
    except SQLAlchemyError as e:
        log.error("Error deleting track -- %s" % str(e))


def getTrack(id):
    return Track.query.filter_by(id=id).first_or_404()


def getAllTracks():
    return Track.query.all();
