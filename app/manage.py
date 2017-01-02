from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

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

if __name__ == '__main__':
    manager.run()
