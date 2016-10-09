from __future__ import unicode_literals
import logging
import os
from logging.handlers import RotatingFileHandler
from flask import (Flask, render_template, request)
from flask.ext.sqlalchemy import SQLAlchemy
from playlist import playlistBlueprint

app = Flask('__name__')
app.register_blueprint(playlistBlueprint)
app.config.update(
    DEBUG=os.environ.get('DEBUG', True),
    SECRET_KEY=os.environ.get('SECRET_KEY', 'set in .env'),
    DATABASE_URL=os.environ.get('DATABASE_URL', 'set in .env'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
db = SQLAlchemy(app)


@app.route('/')
def index():
    '''Render tracklist.'''
    added = request.args.get('added', None)
    return render_template('index.html', added=added)


if __name__ == '__main__':
    if app.debug:
        handler = logging.StreamHandler()
        app.logger.addHandler(handler)
        app.logger.info('stream logger start')
    else:
        handler = RotatingFileHandler('logs/umq.log', maxBytes=10000, backupCount=1)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)

    app.run(debug=app.debug, port=5000, threaded=True)
