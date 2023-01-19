import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

casting_assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlMwN3JYLTlHa1ZlaFl1U1FFSi1qXyJ9.eyJpc3MiOiJodHRwczovL2Rldi1iemhqMHd3dW40MnJjZDgyLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2M2MwYjhjNTJmYmQ3NTE1ZDNmYjkxZGUiLCJhdWQiOiJhZ2VuY3kiLCJpYXQiOjE2NzQwODYzODcsImV4cCI6MTY3NDE3Mjc4NywiYXpwIjoiRkZPTXZ3SnVMZFRGc2xaQUN1YnY4Y0NXQXp6ZlMzMlciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.SrKBqu3XDq6BpqlT8umPoIo3fS16gCEwE9_bOL-SrIORYpGxRyl7YKzBu7-IeUueIJVfqxAg20ZdMCFzJSyJtjV2y_XGr7xc_Da9UZMiDVNrplL4mGSXHXe8yPB9mAGlHTEPrqz3AL7tGc6EWPU4WadFml-9qdDsbcqH7XVaJNB9mWrQ4nWf-EIcRo0exm8Rc1zliXln3tpBFG1fHfMt1MfQOnuYpe7NShXyiphSyIcIZBJGP6dKt7gE14UA91tg8OLtJAEwyP4KOcBPCTXJXlYRoX21mZABKOZh29zxdpY6vQBMcohZomYuu0MTv9cX6wEewm0vJULw2cclEtoHnw'
casting_director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlMwN3JYLTlHa1ZlaFl1U1FFSi1qXyJ9.eyJpc3MiOiJodHRwczovL2Rldi1iemhqMHd3dW40MnJjZDgyLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2M2MwYjk2YTM1ZjhlMjNhZDdlMGEyNzAiLCJhdWQiOiJhZ2VuY3kiLCJpYXQiOjE2NzQwODM5NTQsImV4cCI6MTY3NDE3MDM1NCwiYXpwIjoiRkZPTXZ3SnVMZFRGc2xaQUN1YnY4Y0NXQXp6ZlMzMlciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.rmXeRkV3HPgbewJlmk9vif1TOmOmVcisYD1YqWmGXweD9L7iPLYLjTKAfCrfMQ-qMdJPy1OGtbarxcHtgK-I0vAINWjHBPPxUJRSActKetm9gYOCoZl_wl5uWYdWX388ovqpKcBGp9ZaX9i5-Nt20HvjTlMgYE4fiofMMIdxsl0X7iB9C_vT0ELHMpQKy_I60nwUdA5nZK1J-xmITMK0DYi-xAnnfeAnhfdDYG4LzsGi-8RatO5zJy0mQCO4wFH-3BhT8FJlz3PMY8U_YyoV19AIfdL8KcRHhVu8dP4YBiy19OZZ1f1F9ayoIdJ18FYh_eiNKFFYj-JWOjgRSA652A'
casting_producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlMwN3JYLTlHa1ZlaFl1U1FFSi1qXyJ9.eyJpc3MiOiJodHRwczovL2Rldi1iemhqMHd3dW40MnJjZDgyLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2M2MwYjliYTU0YzU2MWQzM2NlNzZhY2IiLCJhdWQiOiJhZ2VuY3kiLCJpYXQiOjE2NzQwODQ3ODYsImV4cCI6MTY3NDE3MTE4NiwiYXpwIjoiRkZPTXZ3SnVMZFRGc2xaQUN1YnY4Y0NXQXp6ZlMzMlciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.73sY8ZayVuWHJ6UbTL1Oo_3qoy2POz52xUzcDaCkB3OVlllb4UcwLjd3_Oipxd8X1y2ESjSdb2TAl1YzyCxS-D-O8wPNGveTYgacIn7TTaki8iA_FQFcBgY-AlHy2ToOrNcrtkR39WHcLHkXoRmxGx283uAqjNjEs83YjBICuEzuMfPn8RJ4IVwLOQmlKl6ZQOCrxH333IIwhjhvnkcfUt_sBts0Gd_1JpHiZZ94i_eQV-G92zJ56nZvntfVOAUFqb4p2KsZjO6aNrKTRP4Z93_LUcYLoiiWUJ4S8c1EZZ1sf9dg9oAy63CigvQU9R7fdAu3SCOC8eFBTOgp6Krcsw'


class AgencyTestCase(unittest.TestCase):
    """This class represents the agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
        self.DB_USER = os.getenv('DB_USER', 'zhuochen')
        self.DB_NAME = os.getenv('DB_NAME', 'agency')
        self.database_path = "postgresql://{}@{}/{}".format(self.DB_USER, self.DB_HOST, self.DB_NAME)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass


    # GET /actors -- success behavior
    # RBAC for Casting Assistant role -- method allowed
    def test_get_actors(self):
        res = self.client().get('/actors', headers = {'Authorization': 'Bearer ' + casting_assistant_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    # GET /actors -- error behavior
    # Invalid token -- method not allowed
    def test_invalid_token_get_actors(self):
        res = self.client().get('/actors', headers = {'Authorization': 'Bearer ' + 'invalidtoken'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Invalid token.')

    # GET /movies -- success behavior
    # RBAC for Casting Assistant role -- method allowed
    def test_get_movies(self):
        res = self.client().get('/movies', headers = {'Authorization': 'Bearer ' + casting_assistant_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    # GET /movies -- error behavior
    # Invalid token -- method not allowed
    def test_invalid_token_get_movies(self):
        res = self.client().get('/movies', headers = {'Authorization': 'Bearer ' + 'invalidtoken'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Invalid token.')

    # POST /actors -- success behavior
    # RBAC for Casting Director role -- method allowed
    def test_create_actor(self):
        res = self.client().post('/actors', json={'name': 'Tom Cruise', 'age': 60, 'gender': 'male'}, headers = {'Authorization': 'Bearer ' + casting_director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # POST /actors -- error behavior
    # RBAC for Casting Assistant role -- method not allowed
    def test_not_auth_create_actor(self):
        res = self.client().post('/actors', json={'name': 'Michelle Yeoh', 'age': 60, 'gender': 'female'}, headers = {'Authorization': 'Bearer ' + casting_assistant_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')

    # # POST /actors -- error behavior, invalid route
    # # RBAC for Casting Director role -- method allowed
    def test_create_existing_actor(self):
        res = self.client().post('/actors/2', json={'name': 'Johnny Depp', 'age': 59, 'gender': 'male'}, headers = {'Authorization': 'Bearer ' + casting_director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # POST /movies -- success behavior
    # RBAC for Casting Producer role -- method allowed
    def test_create_movie(self):
        res = self.client().post('/movies', json={'title': 'Pirates of the Caribbean', 'release_date': '12022003', 'category': 'adventure'}, headers = {'Authorization': 'Bearer ' + casting_producer_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # POST /movies -- error behavior
    # RBAC for Casting Assistant role -- method not allowed
    def test_not_auth_create_movie(self):
        res = self.client().post('/movies', json={'title': 'Inception', 'release_date': '07162010', 'category': 'action'}, headers = {'Authorization': 'Bearer ' + casting_assistant_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')

    # POST /movies -- error behavior, invalid route
    # RBAC for Casting Director role -- method allowed
    def test_create_existing_movie(self):
        res = self.client().post('/movies/2', json={'title': 'Inception', 'release_date': '07162010', 'category': 'action'}, headers = {'Authorization': 'Bearer ' + casting_director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # PATCH /actors -- success behavior
    # RBAC for Casting Director role -- method allowed
    def test_modify_actor(self):
        res = self.client().patch('/actors/3', json={'age': 61}, headers = {'Authorization': 'Bearer ' + casting_director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_actor'])

    # PATCH /actors -- error behavior, invalid route
    # RBAC for Casting Director role -- method allowed
    def test_invalid_route_modify_actor(self):
        res = self.client().patch('/actors', json={'age': 61}, headers = {'Authorization': 'Bearer ' + casting_director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # PATCH /movies -- success behavior
    # RBAC for Casting Producer role -- method allowed
    def test_modify_movie(self):
        res = self.client().patch('/movies/1', json={'title': 'Superman'}, headers = {'Authorization': 'Bearer ' + casting_producer_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_movie'])

    # PATCH /movies -- error behavior
    # RBAC for Casting Assistant role -- method not allowed
    def test_not_auth_modify_movie(self):
        res = self.client().patch('/movies/1', json={'title': 'Superman'}, headers = {'Authorization': 'Bearer ' + casting_assistant_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')

    # DELETE /actors -- success behavior
    # RBAC for Casting Producer role -- method allowed
    def test_delete_actor_producer(self):
            res = self.client().delete('/actors/8', headers = {'Authorization': 'Bearer ' + casting_producer_token})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['actors'])
            self.assertTrue(data['delete_actor_id'])

    # DELETE /actors -- error behavior, invalid route
    # RBAC for Casting Producer role -- method allowed
    def test_delete_invalid_id_actor(self):
        res = self.client().delete('/actors/100', headers = {'Authorization': 'Bearer ' + casting_producer_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # DELETE /actors -- success behavior
    # RBAC for Casting Director role -- method allowed
    def test_delete_actor_director(self):
            res = self.client().delete('/actors/7', headers = {'Authorization': 'Bearer ' + casting_director_token})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['actors'])
            self.assertTrue(data['delete_actor_id'])

    # DELETE /movies -- success behavior
    # RBAC for Casting Producer role -- method allowed
    def test_delete_movie_producer(self):
            res = self.client().delete('/movies/5', headers = {'Authorization': 'Bearer ' + casting_producer_token})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['movies'])
            self.assertTrue(data['delete_movie_id'])

    # DELETE /movies -- error behavior
    # RBAC for Casting Director role -- method not allowed
    def test_delete_movie_director(self):
            res = self.client().delete('/movies/3', headers = {'Authorization': 'Bearer ' + casting_director_token})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 403)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Permission not found')




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
