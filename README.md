**UMQ (Universal Media Queuer)** is a music streaming web app that can create a playlist from multiple sources (youtube, bandcamp, soundcloud, etc.)

**Demo:** http://umq.herokuapp.com/

## Local Setup

```
$ pip install -r requirements.txt
$ bower install
$ gem install foreman
```

```
$ mongod
$ mongoimport --db umq --collection playlist --drop --file test_playlist.json
```

```
$ foreman start (or python app.py)
```
Runs at [http://localhost:5000](http://localhost:5000)

## Deployment



## TODO

* seek within stream
* multiple playlists
