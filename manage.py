import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from app import app, db


app.config.update(
    DEBUG=os.environ.get('DEBUG', True),
    SECRET_KEY=os.environ.get('SECRET_KEY', 'set in .env'),
    DATABASE_URL=os.environ.get('DATABASE_URL', 'set in .env'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
