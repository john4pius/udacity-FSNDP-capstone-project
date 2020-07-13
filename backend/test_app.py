import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor

EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVNLUoxTTBsSWRYcXZWU0YyYWlTZyJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWZzbmRwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjBhNTdmMjJlYjMwMzAwMTljODY0NjQiLCJhdWQiOiJtb3ZpZXNjYXN0IiwiaWF0IjoxNTk0NTE0MjM4LCJleHAiOjE1OTQ1MjE0MzgsImF6cCI6ImJlTUNJNVg5VTUzWTdjbjR0eXlqVzZCUmI3eVZuVldZIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJERUxFVEU6YWN0b3JzIiwiREVMRVRFOm1vdmllcyIsIkdFVDphY3RvcnMiLCJHRVQ6bW92aWVzIiwiUEFUQ0g6YWN0b3JzIiwiUEFUQ0g6bW92aWVzIiwiUE9TVDphY3RvcnMiLCJQT1NUOm1vdmllcyJdfQ.nDNzrIfQ-LN_8ALly7jVvNeVV5KWhbLrjOCH2c4zhkBtmLKKLIxvAvEEm26K2opLS0dUOtbzwAbYkw9nJAqraPzUupyCaIgFKO7hI73zwPUTecLcoTBEzS6M4G3znbsc_LMKHwKNS_mLnEVyM-zrjmQRxZ28rwNlEquMiy9Uklc8UCFXtYtttvGXBf_WJ9dz-6ljOBvBvcT9paxpyEwgg0LEmUNpQv_EJwu5p8nCt8ZXMb22YIqq4nCiJJTRLO_KMqdN-ys_0DeskMZNZK3NwSpOidTZ68aizv_TSX__h1AFTQlD-G66ndB9k7EwouKKbQQaALc-Oo0D4FDUp0i5zQ'
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVNLUoxTTBsSWRYcXZWU0YyYWlTZyJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWZzbmRwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjBhOGViYzcxNDY4YzAwMTMwMDE3YzIiLCJhdWQiOiJtb3ZpZXNjYXN0IiwiaWF0IjoxNTk0NTI3NzE2LCJleHAiOjE1OTQ1MzQ5MTYsImF6cCI6ImJlTUNJNVg5VTUzWTdjbjR0eXlqVzZCUmI3eVZuVldZIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJERUxFVEU6YWN0b3JzIiwiR0VUOmFjdG9ycyIsIkdFVDptb3ZpZXMiLCJQQVRDSDphY3RvcnMiLCJQQVRDSDptb3ZpZXMiLCJQT1NUOmFjdG9ycyJdfQ.cJ0Dho43oaTnVExVPkIW8blnPjDGjn8CR_OOmc2w5B4GAai-9IgEDC8cixMfdR1CJuHYN4DYIyyNqtOFZv989N4nznyTnBrw1V7VlGjiSxMXKVRR779TlycjrUo2t7REc5DXN4SbwlwT8sCCPgrVHfGw2omfJRVFUxwPDSxTjxGYMHHa2S72_EATgh8smom1ykrbhZI_D1Nxt4Btex-6xyyDUyouxvOwlep-t4qgBJMe68fE2u-Gu6s8n6h4laG1Wbjq70lC06i4PKJsjO_NT1Wx9rMVEqd8q63n17UN6ES4RubeTQ5JkkeVRt4UHZ_zPQeRJhE-zFj56q4DMbw7cg'
CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVNLUoxTTBsSWRYcXZWU0YyYWlTZyJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWZzbmRwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjBhOGU3YmZkMzBlMjAwMTM2NjYwZTYiLCJhdWQiOiJtb3ZpZXNjYXN0IiwiaWF0IjoxNTk0NTI3NTg5LCJleHAiOjE1OTQ1MzQ3ODksImF6cCI6ImJlTUNJNVg5VTUzWTdjbjR0eXlqVzZCUmI3eVZuVldZIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJHRVQ6YWN0b3JzIiwiR0VUOm1vdmllcyJdfQ.lIFiodCieDNj6J0-kzlUQMkzCdF-S_i1R6BZMuZjGuBH38_afOTEABnojUicgjUh2gDUDY8aw9AYLRNko4dnfQw29WNUHpb7WEZKMxjeke0SpMIWvsxUlFhZ38QF5fY-SKi01UzEw4qynocDx1ZpMk4Dt7s2a_yUtFxpZeIMupOfmVr3Brui5eInIs028yOuHbkb0r3MKqxOzhX-ENgHXApbDkrCRwKGT1ustVuM4YHZJcehY4fltTBHM8eoGQZa9qhwvP25jyIAv_ZDa_m8M3w7FXtW4qlvKlJiJmp6MAHwJI0ZgZnUygss_DTTwiD5VOUGjcuGGMhgU5qlIq0BRA'


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

    def test_get_movies(self):
        response = self.client().get(
            '/movies',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

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

    def test_post_movie(self):
        response = self.client().post(
            '/movies',
            json={'title': 'Jumanji', 'release_date': "1981-02-19"},
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



    def test_get_actors(self):
        response = self.client().get(
            '/actors',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])


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


if __name__ == "__main__":
    unittest.main()