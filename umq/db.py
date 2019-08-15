import logging

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger('db')
logger.addHandler(logging.StreamHandler())


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


def addTrack(track):
    try:
        db.session.add(track)
        db.session.commit()
        return track.id
    except SQLAlchemyError as e:
        logging.error("Error adding track -- %s" % str(e))


def deleteTrack(track):
    try:
        db.session.delete(track)
        db.session.commit()
    except SQLAlchemyError as e:
        logging.error("Error deleting track -- %s" % str(e))


def getTrack(id):
    return Track.query.filter_by(id=id).first_or_404()


def getAllTracks():
    return Track.query.all();
