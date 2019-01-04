import db


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
