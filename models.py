from app import app, db


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
        return '<Track id {}>'.format(self.id)

    def add(self, track):
        try:
            db.session.add(track)
            db.session.commit()
            return track.id
        except:
            app.logger.error("Couldn't add to DB.")

    def get(self, id):
        return self.query.filter_by(id=id).first_or_404()

    # def get_all(self):
    #     return self.query.all()
