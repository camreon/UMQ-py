import json
from flask_testing import TestCase
from unittest import mock
from umq.app import create_app
from umq.db import db, Track, Playlist


class ViewsTest(TestCase):

    API_URL = '/api/'
    PLAYLIST_ID = '1'
    NEW_PLAYLIST_URL = 'newplaylist/'

    def create_app(self):

        # pass in test configuration
        test_config = {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "SECRET_KEY": "testing"
        }

        return create_app(test_config)

    def setUp(self):

        db.create_all()

    def tearDown(self):

        db.session.remove()
        db.drop_all()

    def add_track(self, url):

        data = json.dumps(dict(page_url=url))
        res = self.client.post(self.API_URL, data=data, content_type='application/json')

        self.assert200(res)
        self.assertIsNotNone(res.json)
        self.assertNotEqual(len(res.json), 0)

        added_track = res.json[0]
        self.assertEqual(added_track['page_url'], url)

        return added_track['id']

    def test_add_track_to_db_session(self):

        TEST_PAGE_URL = 'test_page_url'
        track = Track(
            title='test_title',
            artist='test_artist',
            page_url=TEST_PAGE_URL,
            stream_url='test_stream_url',
            playlist_id=1
        )
        db.session.add(track)
        db.session.commit()

        self.assertIn(track, db.session)

        res = self.client.get(self.API_URL)

        self.assert200(res)
        self.assertIsNotNone(res.json)
        self.assertNotEqual(len(res.json), 0)

        added_track = res.json[0]
        self.assertEqual(added_track['page_url'], TEST_PAGE_URL)

    def test_empty_db(self):

        res = self.client.get(self.API_URL)

        self.assert200(res)
        self.assertEqual(res.json, [])

    def test_add_tracks(self):

        urls = [
            'https://www.youtube.com/watch?v=c5OS0nALlfQ',
            'http://justcuzurafraidurpeerswillfindou.tumblr.com/post/138394745892/babydreamgirl-babydreamgirl-this-is-the',
            'https://jebediahspringfield.bandcamp.com/track/i-like-killing-flies-2'
        ]

        for url in urls:
            self.add_track(url)

        res = self.client.get(self.API_URL)

        self.assertIsNotNone(res.json)

    def test_add_playlist(self):

        playlist_url = 'https://alldogs.bandcamp.com/album/7'

        data = json.dumps(dict(page_url=playlist_url))
        res = self.client.post(self.API_URL, data=data, content_type='application/json')

        self.assert200(res)
        self.assertIsNotNone(res.json)

        # should add all tracks from the playlist
        added_track = res.json[2]

        self.assertEqual(
            added_track['page_url'],
            playlist_url
        )
        self.assertEqual(
            'mock alt title 3',
            added_track['title']
        )

    def test_add_invalid_tracks(self):

        invalid_urls = [
            'https://p1.bcbits.com/download/track/7a14ab38227d81d996ab84a9650f48bd',
            'https://r18---sn-5uaeznl6.googlevideo.com/videoplayback',
            'xxxoooxxx',
        ]

        with mock.patch(
            'umq.stream_service.MockStreamService.extract_info',
            side_effect=Exception('test error message')
        ):
            for url in invalid_urls:
                data = json.dumps(dict(page_url=url))
                res = self.client.post(self.API_URL, data=data, content_type='application/json')

                self.assert400(res)
                self.assertEqual('test error message', res.json['message'])

    def test_get_tracks(self):

        # add tracks
        urls = [
            'https://www.youtube.com/watch?v=c5OS0nALlfQ',
            'http://justcuzurafraidurpeerswillfindou.tumblr.com/post/138394745892/babydreamgirl-babydreamgirl-this-is-the',
            'https://jebediahspringfield.bandcamp.com/track/i-like-killing-flies-2'
        ]
        for url in urls:
            self.add_track(url)

        # confirm they're there
        res = self.client.get(self.API_URL)

        self.assertIsNotNone(res.json)

        for index, url in enumerate(urls):
            self.assertEqual(
                res.json[index]['page_url'],
                url
            )

    def test_get_track_info(self):

        # add track
        url = 'https://www.youtube.com/watch?v=c5OS0nALlfQ'
        track_id = self.add_track(url)

        # confirm it's there
        res = self.client.get('{}{}/{}'.format(self.API_URL, self.PLAYLIST_ID, track_id))

        self.assertIsNotNone(res.json)
        self.assertEqual(res.json['page_url'], url)

    def test_get_missing_track(self):
        
        track_id = 1000000

        res = self.client.get('{}{}/{}'.format(self.API_URL, self.PLAYLIST_ID, track_id))

        self.assert404(res)

    def test_delete_track(self):

        # add track
        url = 'https://www.youtube.com/watch?v=c5OS0nALlfQ'
        track_id = self.add_track(url)

        # confirm it's there
        res = self.client.get('{}{}/{}'.format(self.API_URL, self.PLAYLIST_ID, track_id))

        self.assertIsNotNone(res.json)
        self.assertEqual(res.json['page_url'], url)

        # delete it
        res = self.client.delete('{}{}/{}'.format(self.API_URL, self.PLAYLIST_ID, track_id))

        self.assert200(res)
        self.assertEqual(res.json['page_url'], url)

        # confirm it was deleted
        res = self.client.get('{}{}/{}'.format(self.API_URL, self.PLAYLIST_ID, track_id))

        self.assert404(res)

    def test_new_playlist(self):
        
        # returns 1 when no playlists exist
        res = self.client.get('{}{}'.format(self.API_URL, self.NEW_PLAYLIST_URL))

        self.assert200(res)
        self.assertEqual(res.json, 1 )

        # add track to add a new playlist 
        url = 'https://www.youtube.com/watch?v=c5OS0nALlfQ'
        self.add_track(url)

        # returns 2 as the next available playlist 
        res = self.client.get('{}{}'.format(self.API_URL, self.NEW_PLAYLIST_URL))

        self.assert200(res)
        self.assertEqual(res.json, 2)
