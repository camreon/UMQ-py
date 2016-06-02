from __future__ import unicode_literals
from flask import Flask, g, render_template, jsonify, abort, flash, \
    redirect, url_for, request
from flask.ext.pymongo import PyMongo
import youtube_dl

app = Flask('__name__')
app.secret_key = 'some_secret'
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.config['MONGO_DBNAME'] = 'umq'
app.debug = True

mongo = PyMongo(app)


@app.before_request
def before_request():
    g.playlist = mongo.db.playlist


@app.route('/')
def index():
    return render_template('index.jade', playlist=g.playlist.find().sort('_id', 1))


@app.route('/playlist/<ObjectId:id>')
def get_track_url(id):
    track = g.playlist.find_one_or_404(id)
    return track['url']


@app.route('/delete/<ObjectId:id>')
def delete_track(id):
    track = g.playlist.find_one_and_delete({'_id': id})
    flash('DELETED: %s - %s' % (track['title'], track['artist']))
    return redirect(url_for('index'))


@app.route('/playlist', methods=['POST'])
def add():
    url = request.form['url']
    with youtube_dl.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)

    if 'entries' in info:
        tracks = info['entries']
    else:
        tracks = [info]

    for t in tracks:
        g.playlist.insert_one({
            'title': t['title'],
            'artist': t.get('artist', ''),
            'url': t['url']
        })
        flash('ADDED: %s' % t['title'])

    return redirect(url_for('index'))


# error handling #
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(400)
def custom400(error):
    # response = jsonify({'message': error.description})
    print(error.description)
    abort(400, error.description)


# @app.errorhandler(404)
# def custom404(error):
#     return render_template('404.jade', error=error)


# Run application
if __name__ == '__main__':
    app.run(debug=True, port=3000)
