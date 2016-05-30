from flask import Flask, g, request, render_template, jsonify, abort
from flask.ext.pymongo import PyMongo

app = Flask('__name__')
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.config['MONGO_DBNAME'] = 'umq'
app.debug = True

mongo = PyMongo(app)


@app.before_request
def before_request():
    g.playlist = mongo.db.playlist


@app.route('/')
def index():
    return render_template('index.jade', playlist=g.playlist.find())


@app.route('/playlist/<ObjectId:id>')
def get_track_url(id):
    track = g.playlist.find_one_or_404(id)
    return track['url']


@app.route('/delete/<id>')
def delete_track(id):
    raise InvalidUsage('This view is unimplemented', status_code=404)


# @app.route('/playlist', methods=['POST'])
# def add():
    #
    # return redirect(url_for('index'))


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


# Run application
if __name__ == '__main__':
    app.run(debug=True, port=3000)
