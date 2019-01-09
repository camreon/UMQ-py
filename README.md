**UMQ (Universal Media Queuer)** is a music streaming web app that can create a playlist from multiple sources (youtube, bandcamp, soundcloud, etc.)

**Demo:** http://umq.herokuapp.com/

#### Local Setup

```
$ pip install -r requirements.txt
$ brew install yarn
$ yarn
$ gem install foreman
```

```
$ foreman start (or python app.py)
```

Runs at [http://localhost:5000](http://localhost:5000)


## Migrations

uses sqlalchemy, alembic, and flask-migrate

```
psql -U postgres -d umq
```
```
CREATE DATABASE umq
```
```
python manage.py db init
```
```
python manage.py db migrate
```
```
python manage.py db upgrade
```

## TODO

- tests
- production config
- CI