from __future__ import unicode_literals

from flask import Flask
from umq.config import get_env_config
from umq.db import db
from umq.views import bp


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    env = get_env_config()

    # some deploy systems set the database url in the environ
    # db_url = os.environ.get("DATABASE_URL")

    # if db_url is None:
    #     default to a sqlite database in the instance folder
        # db_url = "sqlite:///" + os.path.join(app.instance_path, "flaskr.sqlite")
        # ensure the instance folder exists
        # os.makedirs(app.instance_path, exist_ok=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # app.config.from_pyfile("config.py", silent=False)
        app.config.from_mapping(
            SQLALCHEMY_DATABASE_URI=env['sqlalchemy_database_uri'],  # db_url
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            SECRET_KEY=env['secret_key'],
            ECOSYSTEM=env['ecosystem'],
            DEBUG=env['debug']
        )
    else:
        # load the test config if passed in
        app.config.update(test_config)

    db.init_app(app)

    app.register_blueprint(bp)

    # make "index" point at "/", which is handled by "blog.index"
    app.add_url_rule("/", endpoint="index")

    return app
