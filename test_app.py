import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor

EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVNLUoxTTBsSWRYcXZWU0YyYWlTZyJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWZzbmRwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjBhNTdmMjJlYjMwMzAwMTljODY0NjQiLCJhdWQiOiJtb3ZpZXNjYXN0IiwiaWF0IjoxNTk0NjQwNjIwLCJleHAiOjE1OTQ3MjcwMjAsImF6cCI6ImJlTUNJNVg5VTUzWTdjbjR0eXlqVzZCUmI3eVZuVldZIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJERUxFVEU6YWN0b3JzIiwiREVMRVRFOm1vdmllcyIsIkdFVDphY3RvcnMiLCJHRVQ6bW92aWVzIiwiUEFUQ0g6YWN0b3JzIiwiUEFUQ0g6bW92aWVzIiwiUE9TVDphY3RvcnMiLCJQT1NUOm1vdmllcyJdfQ.JbeOjj4DTa3HqyrcgU0m7ucLlGhUe1OY_-WQIXAOzNQZZIHjyrrGSB8uMqbyd8qxjkzQqLggUOM9rEz9Six1rBHUugGqQ-k-p2lumxJyG5iRQvNI53GNwOWZjJu_nw86eFTLP_G20u6NHOknDnrVg8cK8NV7Z_qm0nOitD5EQRILYrLGQSflZeXhHTfbUhBPKDpE1XHXTmHmHzykAO__EEWe9nDsPyECX-sKfmovJOzxZ-r_ygfiBnUVjKpJGe9B5mNywOTMyhnK01RN1XCZq7KmR0LU_BS0b8S2758fjJ_ZkP9MWSFXwaBewYAgMExrbJ-HTzkeLKjQ1g40FDOHOw'
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVNLUoxTTBsSWRYcXZWU0YyYWlTZyJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWZzbmRwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjBhOGViYzcxNDY4YzAwMTMwMDE3YzIiLCJhdWQiOiJtb3ZpZXNjYXN0IiwiaWF0IjoxNTk0NjQwNjkxLCJleHAiOjE1OTQ3MjcwOTEsImF6cCI6ImJlTUNJNVg5VTUzWTdjbjR0eXlqVzZCUmI3eVZuVldZIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJERUxFVEU6YWN0b3JzIiwiR0VUOmFjdG9ycyIsIkdFVDptb3ZpZXMiLCJQQVRDSDphY3RvcnMiLCJQQVRDSDptb3ZpZXMiLCJQT1NUOmFjdG9ycyJdfQ.wL9m3yLSCcAc_hPSnGLOwmfM7eBAx1UUeyDiJIHmen54ZLl4rzzowZ13lDk9lyjo89io-p6WJKPp09sGcdioR61DFEF8nFzcXrqmlENld4rxJfPtPumAABH_NYBFxP2OeBZFZXu5fbU7G_WDmB7sH8t7vxYbUh-GYA-_fHhcYr1O2tyitHD3Lnl2bozdGnlaRAA2tx4GB-Cl9gPiG8YytNe09yeqZvAcmoQDUke4BIwYOd_ZUxmK9fenh5cZCz_Cmx1Yo8oFquRrR4JpiT5uk41vQPDoZWDI60DOwRAg6Di0FUUKLCrtHlic5TPdJChhzQkiYtVClkbQ3Ty3lj5WZw'
CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVNLUoxTTBsSWRYcXZWU0YyYWlTZyJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWZzbmRwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjBhOGU3YmZkMzBlMjAwMTM2NjYwZTYiLCJhdWQiOiJtb3ZpZXNjYXN0IiwiaWF0IjoxNTk0NjQwNzUzLCJleHAiOjE1OTQ3MjcxNTMsImF6cCI6ImJlTUNJNVg5VTUzWTdjbjR0eXlqVzZCUmI3eVZuVldZIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJHRVQ6YWN0b3JzIiwiR0VUOm1vdmllcyJdfQ.ilU_Tu9E0TxDlvsnQoDPt809j0Cf_p-K-vHURFJIPCFyfVO35iuVvtDVhwepVGDrf_uKhx70hvjCU_1qRaUJOxjpCM0d5XM3Vse3NYLIXlFOXHtQZOKKTCkDB3xkEScTOCI4wulrFdJXUweT_nSDAX18H0nNXzo6bI2K_sYMqogSjv0bMEBs7C3Zt0FaQmci0L02YX5hAJVjiaKfHtxJ5CnG80MytrdTl0uTv7mldJb-Bxs3i4KPV7CPmoZCU5p4ca1OrVphAYSOND1cMXF3DJFbeHOKjtshKmVr9aTrwEgksmpbYXOJKzULXuIZfMMx2o9wPEQk-5GPjP7WlSYacw'

class CapstoneTestCase(unittest.TestCase):
    """This class represents the movies-hub test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL']

        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after reach test"""
        pass

    ''' GET /movies '''
    def test_get_movies(self):
        response = self.client().get(
            '/movies',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    ''' GET /movies/id '''
    def test_get_movie_by_id(self):
        response = self.client().get(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Black Panther')

    def test_get_movie_by_id_404(self):
        response = self.client().get(
            '/movies/10000',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['message'], 'Resource not found')

    '''  POST /movies '''
    def test_post_movie(self):
        response = self.client().post(
            '/movies',
            json={'title': 'mission impossible 3', 'release_date': "2006-08-01"},
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie added')
        self.assertEqual(data['movie']['title'], 'Jumanji')

    def test_post_movie_400(self):
        response = self.client().post(
            '/movies',
            json={'title': '', 'release_date': ""},
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    def test_post_movie_401(self):
        response = self.client().post(
            '/movies',
            json={'title': 'Wrong movie', 'release_date': "1984-01-23"},
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

    ''' PATCH /movies '''
    def test_edit_movie(self):
        response = self.client().patch(
            '/movies/2',
            json={'title': 'The Hangover', 'release_date': "2018-10-12"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie updated')
        self.assertEqual(data['movie']['title'], 'The Hangover')

    def test_edit_movie_400(self):
        response = self.client().patch(
            '/movies/1',
            json={'title': '', 'release_date': ""},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    def test_edit_movie_404(self):
        response = self.client().patch(
            '/movies/50000',
            json={'title': 'Black Panther 2', 'release_date': "2019-11-12"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    ''' DELETE /movies/id '''
    def test_delete_movie(self):
        response = self.client().delete(
            '/movies/3',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie deleted')

    def test_delete_movie_404(self):
        response = self.client().delete(
            '/movies/110000',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_movie_401(self):
        response = self.client().delete(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')


    ''' # ==========================================================================================================
    #  GET /actors '''
    def test_get_actors(self):
        response = self.client().get(
            '/actors',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    ''' GET /actors/id '''
    def test_get_actor_by_id(self):
        response = self.client().get(
            '/actors/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'], 'Pierce Brosnan')

    def test_get_actor_by_id_404(self):
        response = self.client().get(
            '/actors/10000',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['message'], 'Resource not found')

    ''' POST /actors '''
    def test_post_actor(self):
        response = self.client().post(
            '/actors',
            json={'name': 'David', 'age': 44, "gender": "male"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor added')
        self.assertEqual(data['actor']['name'], 'David')

    def test_post_actor_400(self):
        response = self.client().post(
            '/actors',
            json={'name': '', 'age': '', "gender": ""},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    def test_post_actor_401(self):
        response = self.client().post(
            '/actors',
            json={'name': 'Jude', 'age': 44, "gender": "male"},
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

    ''' PATCH /actors '''
    def test_edit_actor(self):
        response = self.client().patch(
            '/actors/2',
            json={'name': 'Cynthia', 'age': 27, "gender": "female"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor updated')
        self.assertEqual(data['actor']['name'], 'Cynthia')

    def test_edit_actor_400(self):
        response = self.client().patch(
            '/actors/2',
            json={'name': '', 'age': '', "gender": ""},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    def test_edit_actor_404(self):
        response = self.client().patch(
            '/actors/50000',
            json={'name': 'Cynthia', 'age': 27, "gender": "female"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    ''' DELETE /actors/id '''
    def test_delete_actor(self):
        response = self.client().delete(
            '/actors/3',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor deleted')

    def test_delete_actor_404(self):
        response = self.client().delete(
            '/actors/110000',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_actor_401(self):
        response = self.client().delete(
            '/actors/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

''' Make the tests conveniently executable
if __name__ == "__main__": '''
    unittest.main()