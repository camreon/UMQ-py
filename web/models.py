import db


class Track(db.Model):
    __tablename__ = 'tracks'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    title = db.Column(db.String())
    artist = db.Column(db.String())
    page_url = db.Column(db.String())

    def __init__(self, url, title, artist, page_url):
        self.url = url
        self.title = title
        self.artist = artist
        self.page_url = page_url

    def __repr__(self):
        return '{}'.format(self.id)

    def to_json(self):
        return dict(
            id=self.id,
            url=self.url,
            title=self.title,
            artist=self.artist,
            page_url=self.page_url
        )
